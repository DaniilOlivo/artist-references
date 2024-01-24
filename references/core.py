from django.conf import settings
import json
import random

def get_priority_map():
    with open(settings.BASE_DIR / "references" / "config" / "priority_map.json") as f:
        return json.load(f)

def get_ref(listRefs):
    totals = {}
    running_total = 0

    for ref in listRefs:
        priority_map = get_priority_map()

        w_status = priority_map["priority"][ref.status]
        if w_status == 0:
            continue

        w_tag = 0
        for tag in ref.tags.all():
            w_tag += tag.priority - priority_map["base"]

        w_total = w_status + w_tag
        if w_total <= 0:
            continue
        
        running_total += w_total
        totals[ref.id] = running_total

    rnd = random.random() * running_total
    for id, total in totals.items():
        if rnd < total:
            return id
