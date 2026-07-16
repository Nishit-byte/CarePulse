from database import init_db, add_device, add_person, log_alert, resolve_alert
import time
import random

def seed():
    init_db()

    living_room_id = add_device("Living Room", "online")
    bedroom_id = add_device("Bedroom", "online")
    kitchen_id = add_device("Kitchen", "online")

    you_id = add_person("You", 24, "Living Room", living_room_id, is_live=1)
    robert_id = add_person("Robert Smith", 68, "Bedroom", bedroom_id, is_live=0)
    linda_id = add_person("Linda Brown", 71, "Kitchen", kitchen_id, is_live=0)

    demo_events = [
        (robert_id, bedroom_id, 12, 0.91, "Medium"),
        (linda_id, kitchen_id, 20, 0.87, "Medium"),
        (robert_id, bedroom_id, 25, 0.94, "High"),
    ]

    for person_id, device_id, days_ago, confidence, priority in demo_events:
        ts = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() - days_ago * 86400))
        alert_id = log_alert(person_id, device_id, confidence, priority, timestamp=ts)
        resolve_alert(alert_id, person_id)

    print("Seed complete.")
    print(f"Live person: You (id={you_id}) - Living Room")
    print(f"Demo person: Robert Smith (id={robert_id}) - Bedroom")
    print(f"Demo person: Linda Brown (id={linda_id}) - Kitchen")

if __name__ == "__main__":
    seed()