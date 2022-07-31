from ss13stats import db_ext, ma_ext

from datetime import datetime, timedelta

from sqlalchemy import Column, Integer, DateTime, String, Enum, func

class Server(db_ext.Model):
    __tablename__ = "servers"

    id = Column("id", Integer(), primary_key=True)
    first_seen = Column("first_seen", DateTime())
    last_seen = Column("last_seen", DateTime())
    title = Column("title", String(1024))
    player_count = Column("player_count", Integer())
    online = Column("online", Integer())

    def byond_url(self):
        return f"byond://BYOND.world.{self.id}"
    
    @classmethod
    def get_hub_list(cls):
        return cls.query.filter().order_by(cls.online.desc(), cls.player_count.desc())


class ServerSchema(ma_ext.SQLAlchemyAutoSchema):
    class Meta:
        model = Server


class GlobalStat(db_ext.Model):
    __tablename__ = "global_stats"

    id = Column("id", Integer(), primary_key=True)
    timestamp = Column("timestamp", DateTime())
    type = Column("type", Enum("SERVER_COUNT", "PLAYER_COUNT", "FAN_COUNT"))
    value = Column("value", Integer())

    @classmethod
    def get_stats(cls, type, start=None, end=None, grouping=None, limit=None):
        cur = cls.query.filter(cls.type == type).order_by(cls.timestamp.asc())

        if start:
            cur = cur.filter(cls.timestamp >= start)
        
        if end:
            cur = cur.filter(cls.timestamp <= end)
        
        if grouping:
            if grouping == "HOUR":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y-%m-%d %h"))
            elif grouping == "DAY":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y-%m-%d"))
            elif grouping == "MONTH":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y-%m"))
            elif grouping == "YEAR":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y"))
            
            cur = cur.with_entities(cls.id, cls.timestamp, cls.type, func.avg(cls.value).label("value"))

        if limit:
            cur = cur.limit(limit)

        return cur.all()

class GlobalStatSchema(ma_ext.SQLAlchemyAutoSchema):
    class Meta:
        model = GlobalStat


class ServerStat(db_ext.Model):
    __tablename__ = "server_stats"

    id = Column("id", Integer(), primary_key=True)
    timestamp = Column("timestamp", DateTime())
    server_id = Column("server_id", Integer())
    player_count = Column("player_count", Integer())

    @classmethod
    def get_stats(cls, server_id, start=None, end=None, grouping=None, limit=None):
        cur = cls.query.filter(cls.server_id == server_id).order_by(cls.timestamp.asc())

        if start:
            cur = cur.filter(cls.timestamp >= start)
        
        if end:
            cur = cur.filter(cls.timestamp <= end)
        
        if grouping:
            if grouping == "HOUR":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y-%m-%d %h"))
            elif grouping == "DAY":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y-%m-%d"))
            elif grouping == "MONTH":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y-%m"))
            elif grouping == "YEAR":
                cur = cur.group_by(func.date_format(cls.timestamp, "%Y"))
            
            cur = cur.with_entities(cls.id, cls.timestamp, cls.server_id, func.avg(cls.player_count).label("player_count"))

        if limit:
            cur = cur.limit(limit)

        return cur.all()


class ServerStatSchema(ma_ext.SQLAlchemyAutoSchema):
    class Meta:
        model = ServerStat
