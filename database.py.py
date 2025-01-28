# database.py
class DatabaseManager:
    def __init__(self, config):
        # Existing tables
        self.trades = sa.Table('trades', self.metadata,
            sa.Column('id', sa.Integer, primary_key=True),
            sa.Column('token_address', sa.String(42)),
            sa.Column('action', sa.String(4)),
            sa.Column('amount', sa.Float),
            sa.Column('price', sa.Float),
            sa.Column('timestamp', sa.DateTime)
        )

    def log_trade(self, token, action):
        with self.engine.connect() as conn:
            stmt = self.trades.insert().values(
                token_address=token,
                action=action,
                timestamp=datetime.now()
            )
            conn.execute(stmt)
            conn.commit()