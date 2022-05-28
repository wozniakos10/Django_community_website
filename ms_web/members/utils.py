from datetime import datetime

def compute_user_points(no_comments, no_spots, user_date_joined):
    today = datetime.today()
    joined = user_date_joined
    t = datetime.strptime(str(today)[:10], "%Y-%m-%d")
    j = datetime.strptime(str(joined)[:10], "%Y-%m-%d")
    days = (t-j).days
    return int(no_comments * 2 + no_spots * 3 + days * 0.3)