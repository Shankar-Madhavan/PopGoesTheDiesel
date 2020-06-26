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

    # Calculate 3 markers that are at varying distances away from the center line
    marker_1 = 0.1 * track_width
    marker_2 = 0.20 * track_width
    marker_3 = 0.5 * track_width

    # Give higher reward if the car is closer to center line and vice versa
    if distance_from_center <= marker_1:
        reward = 3
    elif distance_from_center <= marker_2:
        reward = 1
    else:
        reward = 0.00001  # likely crashed/ close to off track
	
    print('distance_from_center '+ str(distance_from_center)+ ' Reward '+ str(reward) )
	
    if reward != 0.00001:
	        
        # Calculate the direction of the center line based on the closest waypoints
        next_point = waypoints[closest_waypoints[1]]
        prev_point = waypoints[closest_waypoints[0]]
        
        # Calculate the direction in radius, arctan2(dy, dx), the result is (-pi, pi) in radians
        track_direction = math.atan2(next_point[1] - prev_point[1], next_point[0] - prev_point[0]) 
        # Convert to degree
        track_direction = math.degrees(track_direction)
		
        straight_track_direction_lower_threshold = 0.0
        straight_track_direction_upper_threshold = 5.0
        steering_lower_threshold_1 = 0.0
        steering_upper_threshold_2 = 2.0
        heading_lower_threshold_1 = 0.0
        heading_upper_threshold_2 = 1.0
        
        speed_threshold_1 = 2.0
        speed_threshold_2 = 1.0
        
        print('track_direction '+str(track_direction)+' speed '+str(speed)+ ' is_offtrack '+str(is_offtrack) +' all_wheels_on_track '+str(all_wheels_on_track) +' heading '+str(heading) +' steering '+str(steering) +' is_left_of_center '+str(is_left_of_center))
		
		##Start rewarding when Straight Track Direction
        if track_direction >= straight_track_direction_lower_threshold and track_direction <= straight_track_direction_upper_threshold:        	        	
        	##Reward when straight be speedy
        	if speed >= speed_threshold_1:
        		reward += 5
        	else:
        		reward += 2
        	
        	print('Straight Track Direction Speedy Reward '+str(reward))
        	
        	#Reward based on steady Steering
        	if steering == steering_lower_threshold_1:
        		reward += 3
        	else:
        		reward = 0.00002
        	
        	print('Straight Track Direction good handle on steering '+str(reward))
        	
        	if reward == 0.00002:
        	    return float(reward)
        	
    
        	if abs(heading) >= heading_lower_threshold_1 and abs(heading) <= heading_upper_threshold_2:
        		reward += 3
        	else:
        		reward = 0.00003
        	
        	print('Straight Track Direction good direction heading '+str(reward))
        	
        	
        	if reward == 0.00003:
        		return float(reward)			
        else:
            curve_track_direction_upper_threshold_1 = 70.0
            curve_track_direction_upper_threshold_2 = 6.0
            curve_track_direction_upper_threshold_3 = 69.0
            DIRECTION_THRESHOLD_1 = 10.0
            DIRECTION_THRESHOLD_2 = 15.0
            DIRECTION_THRESHOLD_3 = 5.0
            speed_threshold_3 = 3
			# Calculate the difference between the track direction and the heading direction of the car
            direction_diff = abs(abs(track_direction) - abs(heading))
            print('direction_diff '+str(direction_diff)) 
			
        	##Reward/Penalize For Curve
            if abs(track_direction) >= curve_track_direction_upper_threshold_1:
            	## Reward when Slowdown in curve
                if speed < speed_threshold_3 and direction_diff <= DIRECTION_THRESHOLD_3:
                	reward += 5
                elif speed < speed_threshold_3:
                	reward += 3
                else:
                	reward = 0.00004

                print('When Curve Slow down Reward '+str(reward))
            
                if reward == 0.00004:
                	return float(reward)
            
                steering_lower_threshold_3 = 15.0
                
                ##Reward to controlled steering when curve
                if steering <= steering_lower_threshold_3 and direction_diff <= DIRECTION_THRESHOLD_2:
                	reward += 5
                else:
                	reward = 0.00005
                
                print('When Curve control steering Reward '+str(reward))
                
                if reward == 0.00005:
                	return float(reward)
            else:				
            	# Penalize the reward if the difference is too large				
            	if direction_diff <= DIRECTION_THRESHOLD_1 and speed >= speed_threshold_2 and speed <= speed_threshold_1:
            		reward += 5
            	else:					
            		reward = 0.00006
            	
            	print('Track and Heading Reward '+str(reward))

	
    return float(reward)