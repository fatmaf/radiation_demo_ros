from shared_python_code.Point import CPoint 
from shared_python_code.Point import LOCATIONS
from cmath import sqrt

class GenerateAtNear(object):
    def __init__(self,near_ep,at_ep):
        self.near_ep = near_ep 
        self.at_ep = at_ep 
        
    def epsilonFromLoc(self,cx,cy,lx,ly,epsilon):
        distance = (cx-lx)*(cx-lx) + (cy-ly)*(cy-ly)
        distance = sqrt(distance)
        if distance < epsilon:
            return True 
        return False 
    
    def distanceFromLocBetween(self,cx,cy,lx,ly,upperBound,lowerBound):
        distance = (cx-lx)*(cx-lx) + (cy-ly)*(cy-ly)
        distance = sqrt(distance)
        if(dist < upperBound):
            if(dist >= lowerBound):
                return True 
        return False         
 
    # ArrayList<Predicate> getNearLocs(double cx, double cy) {
    #     ArrayList<Predicate> nearlocs = new ArrayList<>();
    #     // not excluding at loc, check for this in the beliefs in gwendolen
    #     for (String loc : this.location_coordinates.keySet()) {
    #         if (nearLoc(cx, cy, loc)) {
    #             nearlocs.add(this.near_location_predicates.get(loc));
    #         }
    #     }
    #     return nearlocs;
    # }
    #
    # boolean nearLoc(double cx, double cy, String loc) {
    #     return nearLoc(cx, cy, location_coordinates.get(loc));
    # }
    #
    # boolean nearLoc(double cx, double cy, AbstractMap.SimpleEntry<Double, Double> loc) {
    #     return distanceFromLocBetween(cx, cy, loc.getKey(), loc.getValue(), this.near_error, this.at_epsilon_error);
    # }       

    # Predicate getLoc(double cx, double cy) {
    #     // go over all the location coordinates
    #     for (String loc : this.location_coordinates.keySet()) {
    #         if (atLoc(cx, cy, loc)) {
    #             return this.at_location_predicates.get(loc);
    #         }
    #     }
    #     return null;
    # }
    #
    # boolean atLoc(double cx, double cy, String loc) {
    #     return atLoc(cx, cy, location_coordinates.get(loc));
    # }
    #
    # boolean atLoc(double cx, double cy, AbstractMap.SimpleEntry<Double, Double> loc) {
    #     return epsilonFromLoc(cx, cy, loc.getKey(), loc.getValue(), at_epsilon_error);
    # }
    #
    # ArrayList<Predicate> getNearLocs(double cx, double cy) {
    #     ArrayList<Predicate> nearlocs = new ArrayList<>();
    #     // not excluding at loc, check for this in the beliefs in gwendolen
    #     for (String loc : this.location_coordinates.keySet()) {
    #         if (nearLoc(cx, cy, loc)) {
    #             nearlocs.add(this.near_location_predicates.get(loc));
    #         }
    #     }
    #     return nearlocs;
    # }
    #
    # boolean nearLoc(double cx, double cy, String loc) {
    #     return nearLoc(cx, cy, location_coordinates.get(loc));
    # }
    #
    # boolean nearLoc(double cx, double cy, AbstractMap.SimpleEntry<Double, Double> loc) {
    #     return distanceFromLocBetween(cx, cy, loc.getKey(), loc.getValue(), this.near_error, this.at_epsilon_error);
    # }
    #
    # boolean distanceFromLocBetween(double cx, double cy, double lx, double ly, double upperBound, double lowerBound) {
    #     double dist = (cx - lx) * (cx - lx) + (cy - ly) * (cy - ly);
    #     dist = Math.sqrt(dist);
    #     if (dist < upperBound) {
    #         if (dist >= lowerBound) {
    #             return true;
    #         }
    #
    #     }
    #     return false;
    #
    # }
    #
    # boolean epsilonFromLoc(double cx, double cy, double lx, double ly, double epsilon) {
    #     double dist = (cx - lx) * (cx - lx) + (cy - ly) * (cy - ly);
    #     dist = Math.sqrt(dist);
    #     if (dist < epsilon)
    #         return true;
    #
    #     return false;
    #
    # }