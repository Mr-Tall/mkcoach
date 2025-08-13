from app.tools import recommend_punish

def test_recommend_punish_window():
    out = recommend_punish("Johnny Cage", -12)
    assert all(m.get("startup", 99) <= 12 for m in out)
