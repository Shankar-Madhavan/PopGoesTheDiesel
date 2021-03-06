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
        
    # Set the speed threshold based your action space 
    SPEED_THRESHOLD = 1.0
    
    if not all_wheels_on_track:
        # Penalize if the car goes off track
        reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward *= 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward += 1.0
        
    
    # Steering penality threshold, change the number based on your action space setting
    ABS_STEERING_THRESHOLD = 15

    # Penalize reward if the agent is steering too much
    if steering > ABS_STEERING_THRESHOLD:
        reward *= 0.8
    else:
		# High reward if the car stays dont do zig zag
	    reward += 1.0
	
	
	# Give additional reward if the car pass every 100 steps
    if (steps % 100) == 0:
        reward += 0.3
	
	# additional reward for progress
    if progress > 90:
	    reward += 1.0
    elif progress > 75:
	    reward += 0.8
    elif progress > 45:
	    reward += 0.5
    elif progress > 30:
	    reward += 0.3
	
    return float(reward)