T = 5
N = 5
maxcap = [518
518
518
300
13
]
mincap = [171.6
171.6
191.4
9.114
7.75
]
c = [133.0926834
38.09301158
38.09301158
380.8005667
804.71
] 
startcost = [2700
2700
11550
1607.33
887.52
]

u0= [0
0
0
0
0
]

mindown = [9
9
9
2
2
]

minup = [15
15
15
2
2
]

rampup = [127.4799595
127.4799595
127.4799595
88.758
4.7058024
]

rampdown = [144.6340123
144.6340123
144.6340123
98.7984
5.24699604
]

d= [541.8981574
505.0821018
476.5611462
455.0535403
448.5077472
]

Pkg.checkout("AmplNLWriter")

using JuMP, AmplNLWriter
m = Model(solver = AmplNLSolver("couenne"))
@variable(m, 0 <= u[1:N,1:T] <=1, Int) #on or off
@variable(m, s[1:N,1:T]) # supply 
@variable(m, xup[1:N, 1:T])
@variable(m, xdown[1:N, 1:T])

min_output_constraint = mincap
for i = 1:1:N-1
    min_output_constraint = [min_output_constraint mincap];
end

max_output_constraint = maxcap
for i = 1:1:N-1
    max_output_constraint = [max_output_constraint maxcap];
end

@constraint(m, sum(u[:,1:T].*s, 1) .== d');

@constraint(m, s .<= max_output_constraint);
@constraint(m, s .>= min_output_constraint);

# ramp up
for t = 1:1:T-1
    for i = 1:1:N
        @NLconstraint(m, u[i,t] * u[i,t+1] *(s[i,t+1] - s[i,t]) <= rampup[i]);
    end
end

# ramp down
for t = 1:1:T-1
    for i = 1:1:N
        @NLconstraint(m, u[i,t] * u[i,t+1] *(- s[i,t+1] + s[i,t]) <= rampdown[i]);
    end
end

# up-time 
@constraint(m, xup[:,1] .== u0)
for t = 2:1:T
    for i = 1:1:N
        @NLconstraint(m, xup[i,t] - (xup[i,t-1]+1)*u[i,t-1]*u[i,t] == 0);
    end
end

for t = 2:1:T
    for i = 1:1:N
        @NLconstraint(m, (u[i,t-1]-u[i,t]) * (xup[i, t-1] - minup[i]) >= 0)
    end
end

# down-time
@constraint(m, xdown[:,1] .== ones(N,1) - u0)
for t = 2:1:T
    for i = 1:1:N
        @NLconstraint(m, xdown[i,t] - (xdown[i,t-1]+1)*(u[i,t-1]-1)*(u[i,t]-1) == 0);
    end
end

for t = 2:1:T
    for i = 1:1:N
        @NLconstraint(m, -(u[i,t-1]-u[i,t]) * (xdown[i, t-1] - mindown[i]) >= 0)
    end
end


#@NLobjective(m, Min, sum(sum(c[i] * s[i,t] for t in 1:T) for i in 1:N) + sum( sum(max(u[i,t]-u[i,t-1], 0)*startcost[i] for t in 2:T) for i in 1:N) + sum(max(u[i,1] - u0[i], 0) * startcost[i] for i in 1:N))
@NLobjective(m, Min, sum(sum(c[i] * s[i,t] for t in 1:T) for i in 1:N) )

solve(m)
print(m)


