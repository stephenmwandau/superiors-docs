from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from . import db

class Power(db.Model, SerializerMixin):
    __tablename__ = 'powers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    description = db.Column(db.String)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    hero_powers = db.relationship("HeroPower", backref="power")

    serialize_rules = ("-hero_powers.power",)

    @validates("description")
    def validate_description(self, key, description):
        if not description:
            raise ValueError("Description must be present")

        if len(description) < 20:
            raise ValueError("Description must be at least 20 characters long")

        return description 

    def __repr__(self):
        return f'''Power {self.name} {self.description}'''