from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from models import db, Flashcard

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///flashlearn.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# ---------------- Models ----------------
class Flashcard(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    question = db.Column(db.String(300), nullable=False)
    answer = db.Column(db.String(500), nullable=False)
    tag = db.Column(db.String(100))
    correct_count = db.Column(db.Integer, default=0)
    incorrect_count = db.Column(db.Integer, default=0)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

# ---------------- Routes ----------------

# Homepage - Show all flashcards
@app.route('/')
def index():
    cards = Flashcard.query.order_by(Flashcard.created_at.desc()).all()
    return render_template('index.html', cards=cards)

# Create a new flashcard
@app.route('/create', methods=['GET', 'POST'])
def create():
    if request.method == 'POST':
        question = request.form['question']
        answer = request.form['answer']
        tag = request.form['tag']
        new_card = Flashcard(question=question, answer=answer, tag=tag)
        db.session.add(new_card)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html')

# Edit flashcard
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    card = Flashcard.query.get_or_404(id)
    if request.method == 'POST':
        card.question = request.form['question']
        card.answer = request.form['answer']
        card.tag = request.form['tag']
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('create.html', card=card)

# Delete flashcard
@app.route('/delete/<int:id>')
def delete(id):
    card = Flashcard.query.get_or_404(id)
    db.session.delete(card)
    db.session.commit()
    return redirect(url_for('index'))

# Learn mode (flashcard flipping)
@app.route('/learn')
def learn():
    cards = Flashcard.query.all()
    return render_template('learn.html', cards=cards)

# Track correct/incorrect from JS (optional future AJAX feature)
@app.route('/track/<int:id>', methods=['POST'])
def track(id):
    card = Flashcard.query.get_or_404(id)
    data = request.get_json()
    if data['result'] == 'correct':
        card.correct_count += 1
    else:
        card.incorrect_count += 1
    db.session.commit()
    return jsonify(success=True)

# Dashboard - accuracy by tag
@app.route('/dashboard')
def dashboard():
    tags = db.session.query(Flashcard.tag).distinct()
    stats = []
    for tag in tags:
        tag_name = tag[0]
        cards = Flashcard.query.filter_by(tag=tag_name).all()
        total = len(cards)
        correct = sum(c.correct_count for c in cards)
        attempts = correct + sum(c.incorrect_count for c in cards)
        accuracy = round((correct / attempts) * 100, 2) if attempts > 0 else 0
        stats.append({
            'tag': tag_name,
            'total': total,
            'correct': correct,
            'accuracy': accuracy
        })
    return render_template('dashboard.html', stats=stats)

# Settings Page
@app.route('/settings')
def settings():
    return render_template('settings.html')

# Reset progress
@app.route('/reset_progress', methods=['POST'])
def reset_progress():
    cards = Flashcard.query.all()
    for c in cards:
        c.correct_count = 0
        c.incorrect_count = 0
    db.session.commit()
    return redirect(url_for('dashboard'))

# Delete all flashcards
@app.route('/delete_all_cards', methods=['POST'])
def delete_all_cards():
    db.session.query(Flashcard).delete()
    db.session.commit()
    return redirect(url_for('index'))

# ---------------- Main ----------------
if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

