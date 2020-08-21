from manage import db, app

class Kifu(db.Model):
    __tablename__ = 'kifus'

    id = db.Column(db.Integer, primary_key=True)
    setup = db.Column(db.Text)
    record = db.Column(db.Text)
    note = db.Column(db.Text)
    game_date = db.Column(db.DateTime)

    def __repr__(self):
        return '<User %r>' % (self.nickname)