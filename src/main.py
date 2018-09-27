
from TrafficSimulator.TrafficProfile import TrafficProfile
from TrafficSimulator.Simulator import Simulator

from FailureModel.LstmNet import LstmNet

import os

FAILURE_MODEL = os.path.abspath('FailureModel/saved_model/model')
FAILURE_LOG = os.path.abspath('failure_log.csv')
STATIC_SWITCH_LOG = os.path.abspath('static_switch_log.csv')
PRIMARY_LOG = os.path.abspath('primary_log.csv')


## Create a traffic profile
traffic_p = TrafficProfile(300)

# # ## Create the simulator and give the the traffic profile
# Run the primary system
sim_normal = Simulator()
for new_cars in traffic_p.iter_timesteps():
    sim_normal.run_timestep_primary(new_cars)
sim_normal.flush_states_to_log(PRIMARY_LOG)


# Run the Static switch system
sim_static = Simulator()
for new_cars in traffic_p.iter_timesteps():
    sim_static.run_timestep_static(new_cars)
sim_static.flush_states_to_log(STATIC_SWITCH_LOG)


# Run the Failover System
sim_failover = Simulator()
sim_failover.add_failure_model(LstmNet(FAILURE_MODEL))
# # Run the Failover this is assuming it's already trained
# # let the normal algo take care of the first 100 timesteps
c = 0
for new_cars in traffic_p.iter_timesteps():
    if c<50:
        sim_failover.run_timestep_primary(new_cars)
    else:
        sim_failover.run_timestep_failover(new_cars)
    c += 1
sim_failover.flush_states_to_log(FAILURE_LOG)

sim_failover.state_store[[
    'cars_north_lane',
    'cars_south_lane',
    'cars_east_lane',
    'cars_west_lane',
    'light_state_north']].plot()

import matplotlib.pyplot as plt
plt.show()
