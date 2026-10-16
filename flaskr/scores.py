from flask import (
    Blueprint, abort, flash, g, redirect, render_template, request, url_for
)

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint("scores", __name__, url_prefix="/rounds")


def get_round_or_404(round_id):
    """Fetch a round owned by the current user, or raise 404."""
    db = get_db()
    round_ = db.execute(
        "SELECT * FROM rounds WHERE id = ? AND user_id = ?",
        (round_id, g.user["id"]),
    ).fetchone()

    if round_ is None:
        abort(404, f"Round id {round_id} doesn't exist.")

    return round_


@bp.route("/")
@login_required
def index():
    db = get_db()
    rounds = db.execute(
        "SELECT r.id, r.course_name, r.date_played, r.notes,"
        " (SELECT COUNT(*) FROM players p WHERE p.round_id = r.id) AS player_count,"
        " (SELECT MIN(score) FROM players p WHERE p.round_id = r.id) AS best_score"
        " FROM rounds r WHERE r.user_id = ?"
        " ORDER BY r.date_played DESC, r.id DESC",
        (g.user["id"],),
    ).fetchall()
    return render_template("scores/index.html", rounds=rounds)


@bp.route("/create", methods=("GET", "POST"))
@login_required
def create():
    if request.method == "POST":
        course_name = request.form["course_name"].strip()
        date_played = request.form["date_played"].strip()
        notes = request.form.get("notes", "").strip()
        my_score = request.form.get("my_score", "").strip()

        errors = []
        if not course_name:
            errors.append("Course name is required.")
        if not date_played:
            errors.append("Date played is required.")
        if not my_score or not my_score.isdigit():
            errors.append("Your score is required and must be a number.")

        friend_entries = []
        for i in range(1, 4):
            name = request.form.get(f"friend{i}_name", "").strip()
            score = request.form.get(f"friend{i}_score", "").strip()
            if name and not score:
                errors.append(f"Friend {i} needs a score.")
            elif score and not name:
                errors.append(f"Friend {i} needs a name.")
            elif name and score:
                if not score.isdigit():
                    errors.append(f"Friend {i}'s score must be a number.")
                else:
                    friend_entries.append((name, int(score)))

        if errors:
            for error in errors:
                flash(error, "danger")
            return render_template("scores/create.html")

        db = get_db()
        cur = db.execute(
            "INSERT INTO rounds (user_id, course_name, date_played, notes)"
            " VALUES (?, ?, ?, ?)",
            (g.user["id"], course_name, date_played, notes),
        )
        round_id = cur.lastrowid

        db.execute(
            "INSERT INTO players (round_id, player_name, score) VALUES (?, ?, ?)",
            (round_id, g.user["username"], int(my_score)),
        )
        for name, score in friend_entries:
            db.execute(
                "INSERT INTO players (round_id, player_name, score) VALUES (?, ?, ?)",
                (round_id, name, score),
            )
        db.commit()

        flash("Round saved.", "success")
        return redirect(url_for("scores.view", round_id=round_id))

    return render_template("scores/create.html")


@bp.route("/<int:round_id>")
@login_required
def view(round_id):
    round_ = get_round_or_404(round_id)
    db = get_db()
    players = db.execute(
        "SELECT * FROM players WHERE round_id = ? ORDER BY score ASC",
        (round_id,),
    ).fetchall()
    return render_template("scores/round.html", round=round_, players=players)


@bp.route("/<int:round_id>/delete", methods=("POST",))
@login_required
def delete(round_id):
    get_round_or_404(round_id)
    db = get_db()
    db.execute("DELETE FROM players WHERE round_id = ?", (round_id,))
    db.execute("DELETE FROM rounds WHERE id = ?", (round_id,))
    db.commit()
    flash("Round deleted.", "success")
    return redirect(url_for("scores.index"))
