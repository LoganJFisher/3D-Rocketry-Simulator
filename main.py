GlowScript 2.7 VPython

"Don't touch these variables"
dt = 1.0 #change in time per step
ti = 0.0 #initial time
t = 0.0 #var
v = vec(0.0, 0.0, 0.0) #var
pos = vec(0.0, 0.0, 0.0) #var
vpeak = 0.0 #highest velocity reached
ypeak = 0.0 #highest elevation reached
tpeak = 0.0 #time at which highest point reached
tcrash = 0.0 #time of crash
stage2 = 0.0 #toggle for stage 2
Cd = 0.5 #drag coefficient
p0 = 101.325e3 #sea level atmospheric pressure
L = 0.0065 #temperature lapse rate
T0 = 288.15 #sea level temperature
Ma = 0.0289644 #molar mass of dry air
R = 8.31447 #ideal gas constant
G = 6.67408e-11 #gravitational constant
Me = 5.972e24 #mass of Earth
Re = 6.371e6 #radius of Earth (to sea level)

"You can change these variables"
theta = radians(30.0) #altitude #from x to y #input degrees
phi = radians(20.0) #from x to z #input degrees
Ti1 = 3.0e8 #initial magnitude of thrust for stage 1
Tf1 = Ti1*0.65 #final magnitude of thrust for stage 1
Tt1 = 35 #time at which thrust changes for stage 1 (sudden change)
Mf1 = 1.0e6 #mass of fuel for stage 1
dMf1 = 1.6129e4 #fuel use rate for stage 1
Ti2 = 1.0e8 #initial magnitude of thrust for stage 2
Tf2 = Ti2*0.65 #final magnitude of thrust for stage 2
Tt2 = tpeak+35 #time at which thrust changes for stage 2 (sudden change)
Mf2 = 1.0e6 #mass of fuel for stage 2
dMf2 = 1.6129e4 #fuel use rate for stage 2
Mr = 2.0e6 #mass of rocket
A = 400.0 #surface area of rocket in direction of travel (spherical rocket)
tf = 3.0e4 #max time

"Scene"
scene = display(title='Rocket Launch from Cape Canaveral', width=600, height=200)
Rocket = arrow(pos=vec(0.0,Re-2.85e4,0.0), axis=5e3*v.hat, color=color.red, make_trail=True) #the -2.85e4 is a corrective term because the sphere graphic isn't as big as it should be.
CapeCanaveral = sphere(pos=vec(0.0,Re-2.85e4,0.0), radius=5e4, color=color.yellow)
Earth = sphere(pos=vec(0.0,0.0,0.0), radius=Re, texture=textures.earth)
Earth.rotate(angle=radians(-79.7), axis=vec(1,0,0)) #for the love of god, don't touch these angles
Earth.rotate(angle=radians(27.0), axis=vec(0,1,0))
Earth.rotate(angle=radians(-77.0), axis=vec(0,0,1))

#scene.waitfor('click keydown')
  #press any key to launch
  #uncomment this to make the simulation NOT start automatically

"Motion"
def drag(): #drag
  tempdrag = -0.5*rho1()*Cd*A*vec(sign(v.x)*v.x**2, sign(v.y)*v.y**2, sign(v.z)*v.z**2)
  return(tempdrag)
def da(): #acceleration
  tempa = g+(T+drag())/Mr
  return(tempa)
def dv(): #velocity
  tempv = dt*da(t)
  return(tempv)

"Graphs"
x = graph(x=0, y=0, width=600, height=550, title='rocket position over time', xtitle='time (s)', ytitle='distance (m)', foreground=color.black, background=color.white, fast=False)
xp = gcurve(graph=x, color=color.red)
yp = gcurve(graph=x, color=color.green)
zp = gcurve(graph=x, color=color.blue)
ep = gcurve(graph=x, color=color.magenta)
y = graph(x=0, y=0, width=600, height=550, title='rocket velocity over time', xtitle='time (s)', ytitle='velocity (m/s)', foreground=color.black, background=color.white, fast=False)
xv = gcurve(graph=y, color=color.red)
yv = gcurve(graph=y, color=color.green)
zv = gcurve(graph=y, color=color.blue)
ev = gcurve(graph=y, color=color.magenta)
z = graph(x=0, y=0, width=600, height=550, title='rocket acceleration over time', xtitle='time (s)', ytitle='acceleration (m/s²)', foreground=color.black, background=color.white, fast=False)
xa = gcurve(graph=z, color=color.red)
ya = gcurve(graph=z, color=color.green)
za = gcurve(graph=z, color=color.blue)
ea = gcurve(graph=z, color=color.magenta)
print("For all graphs: red = x, green = y, blue = z, and magenta = magnitude")
print("---")

"---------------------------------------------------------------------------------------"

"While loop"
while t < tf:
  rate(1000)
  t = t+dt
  
  #Distance from center of Earth
  def elevation(): #different than pos.mag because pos.y doesn't include Re
    tempelevation = sqrt(pos.x**(2)+(pos.y+Re)**(2)+pos.z**(2))
    return(tempelevation)
  
  #Gravity
  gvec = Earth.pos-(pos+vec(0.0,Re,0.0))
  gmag = G*Me/(elevation())**2 #changing gravitational acceleration
  g = gmag*gvec.hat
  
  #Drag
  def Temp(): #atmospheric temperature at elevation
    if L*pos.mag < T0:
      tempTemp = T0-L*pos.mag
    else:
      tempTemp = 1e-99
    return(tempTemp)
  def Pressure(): #atmospheric pressure at elevation
    if (L*pos.mag)/T0 < 1:
      tempPressure = p0*(1-(L*pos.mag)/T0)**((g.mag*Ma)/(R*L))
    else:
      tempPressure = 0.0
    return(tempPressure)
  def rho1(): #atmospheric density at pos.y
    temprho1 = (Pressure()*Ma)/(R*Temp())
    return(temprho1)
  
  #Thrust
  if t <= Tt1: #stage 1
    Ts = Ti1
  else:
    Ts = Tf1
  if Mf1 < dMf1 and elevation()-Re < ypeak: #stage 2
    if t <= Tt2:
      Ts = Ti2
      stage2 = 1.0
    else:
      Ts = Tf2
  if Mf1 >= dMf1: #changing total rocket + fuel mass
    Mf1 = Mf1-dMf1
    MR = Mr+Mf1+Mf2
  elif Mf2 >= dMf2 and stage2 == 1.0:
    Mf2 = Mf2-dMf2
    MR = Mr+Mf1+Mf2
  else: #thrust cutoff
    Ts = 0.0
  
  #Motion
  if stage2 == 0.0:
    T = vec(Ts*cos(theta)*cos(phi), Ts*sin(theta), Ts*cos(theta)*sin(phi))
  else:
    T = vec(Ts*v.hat.x, Ts*v.hat.y, Ts*v.hat.z)
  v = v + dv() #velocity
  pos = pos + v*dt #position
    
  #Extrema
  if vpeak < v.mag: #highest velocity reached
    vpeak = v.mag*sin(v.diff_angle(g))
  orb = sqrt(G*Me/elevation()) #minimum orbit velocity
  if elevation()-Re > ypeak: #peak height
    ypeak = elevation()-Re
    tpeak = t
    Tt2 = tpeak+35
  if tpeak > 0.0 and elevation()-Re <= 0.0 and tcrash == 0.0: #time of crash
    tcrash = t
    tf = t
  
  #Plot updates
  xp.plot(t,pos.x)
  xv.plot(t,v.x)
  xa.plot(t,da(t).x)
  yp.plot(t,pos.y)
  yv.plot(t,v.y)
  ya.plot(t,da(t).y)
  zp.plot(t,pos.z)
  zv.plot(t,v.z)
  za.plot(t,da(t).z)
  ep.plot(t,elevation()-Re)
  ev.plot(t,v.mag)
  ea.plot(t,da(t).mag)
  
  #Scene update
  Rocket.pos = pos + vec(0.0, Re-(2.85e4), 0.0)
  if tcrash == 0.0:
    Rocket.axis = 5e3*v.hat

"Output"
if vpeak < orb:
  if tcrash != 0.0:
    print("Your rocket reached a peak height of", ypeak, "m")
    print("---")
    print("Your rocket crashed at t -",tcrash,"s")
  else:
    print("Your rocket reached a height of", ypeak, "m in the alotted", tf, "s")
else:
  print("Your rocket successfully made it to space!")

Rocket.color = color.magenta #Just to make it obvious that the scene has stopped
