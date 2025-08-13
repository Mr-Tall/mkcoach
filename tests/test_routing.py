from app.routing import route_intent

def test_routing_basic():
    assert route_intent("what punishes -12?") == "punish"
    assert route_intent("give me a meterless corner combo") == "combo"
    assert route_intent("what's the startup on b3") == "frame"
    assert route_intent("quiz me on teleport punishes") == "drill"
