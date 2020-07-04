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
    is_left_of_center = params['is_left_of_center']
    is_offtrack = params['is_offtrack']
    steps = params['steps']
    progress = params['progress']
    
    reward = 1e-3
    
    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.25 * track_width
    marker_3 = 0.5 * track_width
        
    # Calculate the direction of the center line based on the closest waypoints
    next_point = waypoints[closest_waypoints[1]]
    prev_point = waypoints[closest_waypoints[0]]
    
    # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
    track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
    # Convert to degree
    track_direction = math.degrees(track_direction)
    
    direction_diff = abs(track_direction - heading)
    if direction_diff > 180:
        direction_diff = 360 - direction_diff
		
    straight_track_direction_lower_threshold = 0.0
    straight_track_direction_upper_threshold = 5.0
        
    speed_threshold_high = 3.0
    speed_threshold_low = 1.0
	
    steering_threshold_1 = 0.0
    steering_threshold_2 = 15.0    
    steering_threshold_3 = 30.0
	
    track_direction_threshold_1 = 0.0
    track_direction_threshold_2 = 1.0
    track_direction_threshold_3 = 5.0
	
    DIRECTION_THRESHOLD_1 = 10.0
    DIRECTION_THRESHOLD_2 = 15.0

    
    within_border = (0.5 * track_width - distance_from_center) >= 0.05
    
    print('track_direction '+str(track_direction)+' speed '+str(speed)+ ' is_offtrack '+str(is_offtrack) +' all_wheels_on_track '+str(all_wheels_on_track) +' heading '+str(heading) +' steering '+str(steering) +' is_left_of_center '+str(is_left_of_center) + ' within_border '+str(within_border)+' direction_diff '+str(direction_diff) + ' distance_from_center '+ str(distance_from_center))
    
	#Rewarded based on within border and all track on wheel
    if all_wheels_on_track and within_border:		
    	reward = 1
    	
    	#Reward when close to center line
    	if distance_from_center <= marker_1:
    		reward += 0.8
    	elif distance_from_center <= marker_2:
    		reward += 0.3
    	elif distance_from_center <= marker_3:
    		reward += 0.1
    	else:
    		reward *= 0.1
    	
    	print('Distance from center Reward '+str(reward))
		
    	if reward > 1:
        	#Reward Based on Speedy
        	reward += (speed/speed_threshold_high) ** 2
        	
        	#Penalize based on steering angle if track direction is straight or curve
        	if track_direction >= track_direction_threshold_1 and track_direction <= track_direction_threshold_2 and steering > steering_threshold_1:
        	    reward *= 0.1
        	elif track_direction >= track_direction_threshold_3 and steering < steering_threshold_2:
        	    reward *= 0.1
        	elif steering > steering_threshold_2:
        	    reward *= 0.5
        	else:
        	    reward += 1
        	    if speed == speed_threshold_high:
        	        reward += 0.8

        	print('Speed And Steering Reward '+str(reward))

    	if reward > 1:
        	#Reward Based on Direction
        	if direction_diff <= DIRECTION_THRESHOLD_1 and steering < steering_threshold_3:
        	    reward += 1
        	elif direction_diff > DIRECTION_THRESHOLD_1 and direction_diff < DIRECTION_THRESHOLD_2 and steering < steering_threshold_3:
        	    reward += 0.5
        	else:
        	    reward *= 0.1
        	    
        	print('Direction Reward '+str(reward))

    	

    print('Final Reward '+str(reward) + ' track_direction '+str(track_direction)+' speed '+str(speed)+ ' is_offtrack '+str(is_offtrack) +' all_wheels_on_track '+str(all_wheels_on_track) +' heading '+str(heading) +' steering '+str(steering) +' is_left_of_center '+str(is_left_of_center) + ' within_border '+str(within_border)+' direction_diff '+str(direction_diff) + ' distance_from_center '+ str(distance_from_center))
    
    return float(reward)