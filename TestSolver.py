from numpy import array, arange, zeros, transpose
from matplotlib import pyplot, rc
from math import pi

def Euler_solver(fcn, x_0, tspan, tstep):
    '''!@brief        Implements a first-order forward euler solver
        @param fcn    A function handle to the function to solve
        @param x_0    The initial value of the state vector
        @param tspan  A span of time over which to solve the system specified as a list
                      with two elements representing initial and final time values
        @param tstep  The step size to use for the integration algorithm
        @return       A tuple containing both an array of time values and an array
                      of output values
    '''
    
    # Define a column of time values
    tout = arange(tspan[0], tspan[1]+tstep, tstep)

    # Preallocate an array of zeros to store state values
    xout = zeros([len(tout)+1,len(x_0)])
    
    # Determine the dimension of the output vector
    r = len(fcn(0,x_0)[1])
    
    # Preallocate an array of zeros to store output values
    yout = zeros([len(tout),r])

    # Initialize output array with intial state vector
    xout[0][:] = x_0.transpose()

    # Iterate through the algorithm but stop one cycle early because
    # the algorithm predicts one cycle into the future
    for n in range(len(tout)):
        
        # Pull out a row from the solution array and transpose to get
        # the state vector as a column
        x = xout[[n]].transpose()
        
        # Pull out the present value of time
        t = tout[n]
        
        # Evaluate the function handle at the present time with the
        # present value of the state vector to compute the derivative
        xd, y = fcn(t, x)
        
        # Apply the update rule for Euler's method. The derivative value
        # must be transposed back to a row here for the dimensions to line up.
        xout[n+1] = xout[n] + xd.transpose()*tstep
        yout[n] = y.transpose()
    
    return tout, yout

def system_eqn_OL(t, x):
    '''!@brief      Implements both state equations and output equations for the open loop system
        @param t    The value of time for a given simulation step
        @param x    The value of the state vector for a given simulation step
        @return     A tuple containing both the derivative of the state vector and the output
                    vector for a given simulation step
    '''
    
    # Constant input voltage for open-loop
    # The voltage must be packed in a 1x1 matrix for the arithmetic below
    u = array([ [12] ]);
    
    # State equations
    xd =  A@x+B@u;
    
    # Output Equations
    y  =  C@x+D@u;
    
    return xd, y

def system_eqn_CL(t, x):
    '''!@brief      Implements both state equations and output equations for the open loop system
        @param t    The value of time for a given simulation step
        @param x    The value of the state vector for a given simulation step
        @return     A tuple containing both the derivative of the state vector and the output
                    vector for a given simulation step
    '''
    
    # Applied motor voltage is proportional to error in motor angle
    V_m = k_p*(th_des - x[2,0]) + k_d*(om_des - x[1,0])
    
    # For a more realistic simulation, the motor voltage will be saturated at 12V
    V_m = min(max(V_m,-12),12)
    
    # The input must be packed into a 1x1 matrix for the arithmetic below
    u = array([ [V_m] ]);
    
    # State equations
    xd =  A@x+B@u;
    
    # Output Equations
    y  =  C@x+D@u;
    
    return xd, y

def RK4_solver(fcn, x_0, tspan, tstep):
    '''!@brief        Implements a fourth-order Runge-Kutta Method
        @param fcn    A function handle to the function to solve
        @param x_0    The initial value of the state vector
        @param tspan  A span of time over which to solve the system specified as a list
                      with two elements representing initial and final time values
        @param tstep  The step size to use for the integration algorithm
        @return       A tuple containing both an array of time values and an array
                      of output values
    '''
    # Define a column of time values
    tout = arange(tspan[0], tspan[1]+tstep, tstep)

    # Preallocate an array of zeros to store state values
    xout = zeros([len(tout)+1,len(x_0)])
    
    # Determine the dimension of the output vector
    r = len(fcn(0,x_0)[1])
    
    # Preallocate an array of zeros to store output values
    yout = zeros([len(tout),r])

    # Initialize output array with intial state vector
    xout[0][:] = x_0.transpose()

    # Iterate through the algorithm but stop one cycle early because
    # the algorithm predicts one cycle into the future
    for n in range(len(tout)):
        # Pull out a row from the solution array and transpose to get
        # the state vector as a column
        x = xout[[n]].transpose()
        # Pull out the present value of time
        t = tout[n]
        k1, y = fcn(t,x)
        temp1 = (t + (.5) * tstep)
        temp2 = x + (.5)*(k1 * tstep)
        k2, y = fcn(temp1, temp2)
        temp2 = x + (.5)*(k2 * tstep)
        k3, y = fcn(temp1, temp2)
        temp1 = t + tstep
        temp2 = x + k3*(tstep)
        k4, y = fcn(temp1, temp2)

        xout[n+1] = xout[n] + (1/6)*(k1 + 2*k2 + 2*k3 + k4).transpose()*tstep
        yout[n] = y.transpose()

    return tout, yout

# Electromechanical properties
J      = 6.8e-7     # Mass moment of inertia   [kg*m^2]
b      = 0          # Viscous damping          [N*m*s/rad]
Kt     = 0.0263     # Torque Constant          [N*m/A]
Kv     = Kt         # Back-emf Constant        [V*s/rad]
R      = 9.00       # Terminal Resistance      [ohm]
L      = 4.72e-3    # Terminal Inductance      [H]

# Parameters for closed-loop model
th_des = 2*pi;      # Desired motor angle      [rad]
om_des = 0;         # Desired motor speed      [rad/s]
k_p    = 7;         # Proportional gain        [V/rad]
k_d    = 0.1;       # Derivative gain          [V*s/rad]

# State-to-state coupling matrix
A = array([ [-R/L,  -Kt/L, 0 ],
            [ Kt/J, -b/J,  0 ],
            [ 0,     1,    0 ] ])

# Input-to-state coupling matrix
B = array([ [1/L],
            [ 0 ],
            [ 0 ] ])

# State-to-output coupling matrix
C = array([ [1, 0, 0],
            [0, 1, 0],
            [0, 0, 1],
            [0, 0, 0] ])

# Input-to-output coupling matrix
D = array([ [0],
            [0],
            [0],
            [1] ])

# The following initial conditions will be used by both the open-loop and
# closed-loop simulations
x_0 = array([ [0],
              [0],
              [0] ])
# Solve the open loop system over a 0.1 second time window with 1 ms steps
t_CL, y_CL = RK4_solver(system_eqn_CL, x_0, [0, 0.1], 1e-6)

# Enlarge font size
rc('font', **{'size'   : 16})

pyplot.figure(figsize=(12,6))
pyplot.plot(t_CL, y_CL[:,1])
pyplot.xlabel('Time, t [s]')
pyplot.ylabel('Motor Velocity, [rad/s]')
pyplot.grid()
pyplot.show()