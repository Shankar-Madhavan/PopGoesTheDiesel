import math

def reward_function(params):
    '''
    Example of rewarding the agent to follow center line
    '''
    
    # Read input parameters
    track_width = params['track_width']
    distance_from_center = params['distance_from_center']
    steering = abs(params['steering_angle']) # Only need the absolute steering angle
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']
    steps = params['steps']
    progress = params['progress']
    waypoints = params['waypoints']
    closest_waypoints = params['closest_waypoints']
    heading = params['heading']
	
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 1.0
    elif distance_from_center <= marker_2:
        reward = 0.5
    elif distance_from_center <= marker_3:
        reward = 0.1
    else:
        reward = 1e-3  # likely crashed/ close to off track
	
    if not reward == 1e-3:
        # Calculate the direction of the center line based on the closest waypoints
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
        
        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
        # Convert to degree
        track_direction = math.degrees(track_direction)
        
        # Calculate the difference between the track direction and the heading direction of the car
        direction_diff = abs(track_direction - heading)
        if direction_diff > 180:
        	direction_diff = 360 - direction_diff
        
        # Penalize the reward if the difference is too large
        DIRECTION_THRESHOLD = 10.0
        if direction_diff > DIRECTION_THRESHOLD:
        	reward *= 0.5
        else:
        	reward += 0.5
    
    # Set the speed threshold based your action space 
    if not reward == 1e-3:
    	SPEED_THRESHOLD = 1.0
    	if not all_wheels_on_track:
    		# Penalize if the car goes off track
    		reward = 1e-3
    	elif speed < SPEED_THRESHOLD:
    		# Penalize if the car goes too slow
    		reward *= 0.5
    	else:
    		# High reward if the car stays on track and goes fast
    		reward += 0.5
    
    
    # Steering penality threshold, change the number based on your action space setting
    if not reward == 1e-3:
    	ABS_STEERING_THRESHOLD = 20
    
    	# Penalize reward if the agent is steering too much
    	if steering > ABS_STEERING_THRESHOLD:
    		reward *= 0.8
    	else:
    		# High reward if the car stays dont do zig zag
    		reward += 0.5
		
	
	
    return float(reward)