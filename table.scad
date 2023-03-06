$fn=1204;
W = 1140;
L = 2600;
Th = 30;
RW = 90;
Cd = L - W;

rotate([0, 0, 90]) {
color("#32946a")
intersection() {
    hull() {
        translate([0, -Cd/2, 0]) cylinder(h=Th, d=W, center=true);
        translate([0, +Cd/2, 0]) cylinder(h=Th, d=W, center=true);
    }
    translate([-210,-40,-49990]) sphere(d=100000);
}

color("#938e81") {
translate([0,Cd/2,-15]) rotate_extrude(angle=180,$fn=195) hull(){
    translate([(W+RW-Th)/2, 0, Th/2]) scale([1, 0.5, 1]) circle(d=Th*3);
}
translate([0,-Cd/2,-15]) rotate_extrude(angle=-180,$fn=195) hull(){
    translate([(W+RW-Th)/2, 0, Th/2]) scale([1, 0.5, 1]) circle(d=Th*3);
}
translate([0,Cd/2,-15]) rotate([90,0,0]) linear_extrude(Cd)
    translate([(W+RW-Th)/2, 0, Th/2]) scale([1, 0.5, 1]) circle(d=Th*3);
translate([0,Cd/2,-15]) rotate([90,0,0]) linear_extrude(Cd)
    translate([(-W-RW+Th)/2, 0, Th/2]) scale([1, 0.5, 1]) circle(d=Th*3);
}
}
