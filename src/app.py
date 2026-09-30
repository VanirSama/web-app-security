from flask import Flask, render_template, redirect, url_for, request, flash, abort
from flask_login import LoginManager, login_user, login_required, logout_user, current_user
from pathlib import Path
from dataclasses import dataclass, asdict
from tomllib import load
import markdown, bleach

from src.config import Config
from src.models import db, UserModel, NoteModel
from src.forms import RegistrationForm, LoginForm, NoteForm, DeleteNoteForm

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"
login_manager.login_message = "Пожалуйста, войдите для доступа к заметкам."
login_manager.login_message_category = "error"


@login_manager.user_loader
def load_user(user_id): return db.session.get(UserModel, int(user_id))

@app.template_filter("markdown")
def render_markdown(text):
    if not text: return ""

    allowed_tags = [
        "p", "b", "i", "strong", "em", "a", "code", "pre", "blockquote",
        "ul", "ol", "li", "h1", "h2", "h3", "h4", "h5", "h6", "hr", "br", "u",
        "table", "thead", "tbody", "tr", "th", "td", "del", "ins", "sub", "sup"
    ]
    allowed_attrs = {
        "a": ["href", "title", "target", "rel"],
        "code": ["class"]
    }
    raw_html = markdown.markdown(text, extensions=["fenced_code", "tables", "nl2br"])
    clean_html = bleach.clean(raw_html, tags=allowed_tags, attributes=allowed_attrs, strip=True)
    clean_html = bleach.linkify(clean_html, skip_tags=["pre"])

    return clean_html


@app.route("/")
def index():
    if current_user.is_authenticated:
        notes = NoteModel.query.filter_by(user_id=current_user.id).order_by(NoteModel.created_at.desc()).all()
        form = NoteForm()
        delete_form = DeleteNoteForm()

        return render_template("index.html", notes=notes, form=form, delete_form=delete_form)

    return render_template("index.html", notes=None, form=None, delete_form=None)


@app.route("/register", methods=["GET", 'POST'])
def register():
    if current_user.is_authenticated: return redirect(url_for("index"))
    form = RegistrationForm()

    if form.validate_on_submit():
        user = UserModel(username=form.username.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Вы успешно зарегистрировались. Войдите в систему.", "success")

        return redirect(url_for("login"))

    return render_template("register.html", form=form)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated: return redirect(url_for("index"))

    form = LoginForm()
    if form.validate_on_submit():
        user = UserModel.query.filter_by(username=form.username.data).first()

        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')

            if next_page and next_page.startswith('/'): return redirect(next_page)

            return redirect(url_for("index"))

        flash("Неверное имя пользователя или пароль", "error")

    return render_template("login.html", form=form)


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/note/create', methods=['POST'])
@login_required
def create_note():
    form = NoteForm()

    if form.validate_on_submit():
        note = NoteModel(title=form.title.data, content=form.content.data, user_id=current_user.id)
        db.session.add(note)
        db.session.commit()
        flash("Заметка создана.", "success")

    else:
        for field, errors in form.errors.items():
            for error in errors: flash(error, "error")

    return redirect(url_for("index"))


@app.route("/note/<int:note_id>/edit", methods=["GET", "POST"])
@login_required
def edit_note(note_id):
    note = db.session.get(NoteModel, note_id) or abort(404)

    if note.user_id != current_user.id: abort(403)

    form = NoteForm()
    if request.method == "GET":
        form.title.data = note.title
        form.content.data = note.content

    elif form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data
        db.session.commit()
        flash("Заметка обновлена.", "success")

        return redirect(url_for("index"))

    else:
        for field, errors in form.errors.items():
            for error in errors: flash(error, "error")

    return render_template("edit.html", form=form, note=note)


@app.route("/note/<int:note_id>/delete", methods=["POST"])
@login_required
def delete_note(note_id):
    form = DeleteNoteForm()

    if not form.validate_on_submit():
        if form.errors.get('csrf_token'):
            flash('Ошибка проверки CSRF-токена. Попробуйте обновить страницу.', 'error')
            return redirect(url_for('index'))

    note = db.session.get(NoteModel, note_id) or abort(404)

    if note.user_id != current_user.id: abort(403)

    db.session.delete(note)
    db.session.commit()
    flash("Заметка удалена.", "success")

    return redirect(url_for("index"))


@app.errorhandler(403)
def forbidden(e): return render_template("error.html", code=403, message="Request Forbidden"), 403

@app.errorhandler(404)
def not_found(e): return render_template("error.html", code=404, message="Page Not Found"), 404

@app.errorhandler(500)
def server_error(e): return render_template("error.html", code=500, message="Internal Server Error"), 500


@dataclass
class DevConfig:
    debug: bool     = False
    host: str       = "127.0.0.1"
    port: int       = 5000

    def load(self) -> dict[str, type]:
        config_file = Path(__file__).parent / "app.dev.toml"
        try:
            cfg = load(config_file.open("rb"))
            self.debug  = cfg.get("DEBUG", False)
            self.host   = cfg.get("HOST", "127.0.0.1")
            self.port   = cfg.get("PORT", 5000)
        except FileNotFoundError: ...

        return asdict(self)


if __name__ == '__main__':
    with app.app_context(): db.create_all()
    app.run(**DevConfig().load())