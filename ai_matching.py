from math import radians, sin, cos, sqrt, atan2

def get_distance(lat1, lon1, lat2, lon2):
    R = 6371  # radius
    dlat = radians(lat2 - lat1)
    dlon = radians(lon2 - lon1)


    a = sin(dlat/2)**2 + cos(radians(lat1)) * cos(radians(lat2)) * sin(dlon/2)**2
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return R * c


def calculate_price(base_price, distance):
    # Add 10 pounds for every 1meter
    return base_price + (distance * 10)


def match_worker(user_lat, user_lng, category, workers_list):
    
    filtered = [w for w in workers_list if w["category"].lower() == category.lower()]

    if not filtered:
        return None

    for w in filtered:
        
        dist = get_distance(user_lat, user_lng, w["location"]["lat"], w["location"]["lng"])
        w["distance"] = round(dist, 2) #two decimals
        
        # Final price
        w["final_price"] = round(calculate_price(w["base_price"], dist), 2)
        
        
        w["score"] = round(w["final_price"] + dist, 2)

    best_worker = sorted(filtered, key=lambda x: x["score"])[0]
    return best_worker