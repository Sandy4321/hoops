from hoopsapp import db


class Teams(db.Model):
    TEAM_ID = db.Column(db.Integer, primary_key=True)
    TEAM_NAME = db.Column(db.String(80))
    GP = db.Column(db.Integer)
    W = db.Column(db.Integer)
    L = db.Column(db.Integer)
    W_PCT = db.Column(db.Float)
    MIN = db.Column(db.Integer)
    OFF_RATING = db.Column(db.Float)
    DEF_RATING = db.Column(db.Float) 
    NET_RATING = db.Column(db.Float) 
    AST_PCT = db.Column(db.Float) 
    AST_TO = db.Column(db.Float)
    AST_RATIO = db.Column(db.Float)
    OREB_PCT = db.Column(db.Float)
    DREB_PCT = db.Column(db.Float) 
    REB_PCT = db.Column(db.Float)
    TM_TOV_= db.Column(db.Float)
    EFG_PCT = db.Column(db.Float)
    TS_PCT = db.Column(db.Float)
    PACE = db.Column(db.Float)
    PIE = db.Column(db.Float)
    CFID = db.Column(db.Integer)
    CFPARAMS = db.Column(db.Text)


    def __init__(self, TEAM_ID, TEAM_NAME, GP, W, L, W_PCT, MIN, OFF_RATING,
                DEF_RATING, NET_RATING, AST_PCT, AST_TO, AST_RATIO, OREB_PCT,
                DREB_PCT, REB_PCT, TM_TOV, EFG_PCT, TS_PCT, PACE, PIE, CFID,
                CFPARAMS):
    
        self.TEAM_ID = TEAM_ID
        self.TEAM_NAME = TEAM_NAME
        self.GP = GP
        self.W = W
        self.L = L
        self.W_PCT = W_PCT
        self.MIN = MIN
        self.OFF_RATING = OFF_RATING
        self.DEF_RATING = DEF_RATING
        self.NET_RATING = NET_RATING
        self.AST_PCT = AST_PCT
        self.AST_TO = AST_TO
        self.AST_RATIO = AST_RATIO
        self.OREB_PCT = OREB_PCT
        self.DREB_PCT = DREB_PCT
        self.REB_PCT = REB_PCT
        self.TM_TOV = TM_TOV
        self.EFG_PCT = EFG_PCT
        self.TS_PCT = TS_PCT
        self.PACE = PACE
        self.PIE = PIE
        self.CFID = CFID
        self.CFPARAMS = CFPARAMS

class Players(db.Model):
    TEAM_ID = db.Column(db.Integer) 
    TEAM_NAME = db.Column(db.String(80))
    PLAYER_ID = db.Column(db.Integer, primary_key=True)
    PLAYER_NAME = db.Column(db.String(80))
    PST = db.Column(db.Float)
    AST = db.Column(db.Float)
    REB = db.Column(db.Float)
    PIE = db.Column(db.Float)

    def __init__(self, TEAM_ID, TEAM_NAME, PLAYER_ID, PLAYER_NAME, PST, AST,
                REB, PIE):

            self.TEAM_ID = TEAM_ID
            self.TEAM_NAME = TEAM_NAME
            self.PLAYER_ID = PLAYER_ID
            self.PLAYER_NAME = PLAYER_NAME
            self.PST = PST
            self.AST = AST
            self.REB = REB
            self.PIE = PIE
