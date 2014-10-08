from application import db


class Historical(db.Model):
    """
    Model for storage.db, ultimately wrapped in S3Shaped
    when returned to 'service'.
    """

    __tablename__ = 'historical'

    key = db.Column(db.String(), nullable=False, primary_key=True)
    value = db.Column(db.String(), nullable=False)
    version = db.Column(db.String(), nullable=False, primary_key=True)
    added = db.Column(db.Integer(), nullable=False)

    def __repr__(self):
        d = {
            'key': self.key,
            'value': self.value,
            'version': self.version,
            'added': self.added
        }
        return str(d)