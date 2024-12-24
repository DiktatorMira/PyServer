class User(Base):
    __tablename__ = 'users'

    def to_dict(self):
        return {
            'user_id': self.user_id,
            'email': self.email,
            'name': self.name,
            'created_date': self.created_date.isoformat(), 
            'last_activity': self.last_activity.isoformat(),
            'status': self.status
        }