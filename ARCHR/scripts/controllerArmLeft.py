#!/usr/bin/env python
# Project ARCHR: Mannan Javid (mannanj90@gmail.com) 
# 		  		 Patrick Early
#          		 Eric Eide
#         	     Martyna Bula
# Copyright (c) 2013-2014, Rethink Robotics
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:
#
# 1. Redistributions of source code must retain the above copyright notice,
#    this list of conditions and the following disclaimer.
# 2. Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in the
#    documentation and/or other materials provided with the distribution.
# 3. Neither the name of the Rethink Robotics nor the names of its
#    contributors may be used to endorse or promote products derived from
#    this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE
# ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT OWNER OR CONTRIBUTORS BE
# LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR
# CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF
# SUBSTITUTE GOODS OR SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS
# INTERRUPTION) HOWEVER CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN
# CONTRACT, STRICT LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE)
# ARISING IN ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.

"""
Baxter RSDK Joint Trajectory Action Client Example
"""
import argparse
import sys

from copy import copy

import rospy

import actionlib

from control_msgs.msg import (
    FollowJointTrajectoryAction,
    FollowJointTrajectoryGoal,
)
from trajectory_msgs.msg import (
    JointTrajectoryPoint,
)

import baxter_interface

from baxter_interface import CHECK_VERSION

# Hubo-ach stuff
import hubo_ach as ha
import ach
from ctypes import *
import time

# feed-forward will now be refered to as "state"
state = ha.HUBO_STATE()
# feed-back will now be refered to as "ref"
ref = ha.HUBO_REF()
# Get the current feed-forward (state) 
r = ach.Channel(ha.HUBO_CHAN_REF_NAME)
[statuss, framesizes] = r.get(ref, wait=False, last=True)


class Trajectory(object):
    def __init__(self, limb):
        ns = 'robot/limb/' + limb + '/'
        self._client = actionlib.SimpleActionClient(
            ns + "follow_joint_trajectory",
            FollowJointTrajectoryAction,
        )
        self._goal = FollowJointTrajectoryGoal()
        server_up = self._client.wait_for_server(timeout=rospy.Duration(10.0))
        if not server_up:
            rospy.logerr("Timed out waiting for Joint Trajectory"
                         " Action Server to connect. Start the action server"
                         " before running example.")
            rospy.signal_shutdown("Timed out waiting for Action Server")
            sys.exit(1)
        self.clear(limb)

    def add_point(self, positions, time):
        point = JointTrajectoryPoint()
        point.positions = copy(positions)
        point.time_from_start = rospy.Duration(time)
        self._goal.trajectory.points.append(point)

    def start(self):
        self._goal.trajectory.header.stamp = rospy.Time.now()
        self._client.send_goal(self._goal)

    def stop(self):
        self._client.cancel_goal()

    def wait(self, timeout=15.0):
        self._client.wait_for_result(timeout=rospy.Duration(timeout))

    def result(self):
        return self._client.get_result()

    def clear(self, limb):
        self._goal = FollowJointTrajectoryGoal()
        self._goal.trajectory.joint_names = [limb + '_' + joint for joint in \
            ['s0', 's1', 'e0', 'e1', 'w0', 'w1', 'w2']]


def main():
    """RSDK Joint Trajectory Example: Simple Action Client

    Creates a client of the Joint Trajectory Action Server
    to send commands of standard action type,
    control_msgs/FollowJointTrajectoryAction.

    Make sure to start the joint_trajectory_action_server.py
    first. Then run this example on a specified limb to
    command a short series of trajectory points for the arm
    to follow.
    """
    s0 = 0;
    s1= -0;
    e0 = 0;
    e1 = 0;
    w0 = 0;
    w1 = 0;
    w2 = 0;

    arg_fmt = argparse.RawDescriptionHelpFormatter
    parser = argparse.ArgumentParser(formatter_class=arg_fmt,
                                     description=main.__doc__)
    required = parser.add_argument_group('required arguments')
    required.add_argument(
        '-l', '--limb', required=True, choices=['left', 'right'],
        help='send joint trajectory to which limb'
    )
    args = parser.parse_args(rospy.myargv()[1:])
    limb = args.limb

    print("Initializing node... ")
    rospy.init_node("rsdk_joint_trajectory_client_%s" % (limb,))
    print("Getting robot state... ")
    rs = baxter_interface.RobotEnable(CHECK_VERSION)
    print("Enabling robot... ")
    rs.enable()
    print("Running. Ctrl-c to quit")
    positions = {
        #'left':  [-0.11, -0.62, -1.15, 1.32,  0.80, 1.27,  2.39],
        #'right':  [0.11, -0.62,  1.15, 1.32, -0.80, 1.27, -2.39],
        'left':  [s0, s1, e0, e1,  w0, w1,  w2],
        'right':  [-s0, s1, -e0, e1,  -w0, w1,  -w2],

    }
    
    traj = Trajectory(limb)
    rospy.on_shutdown(traj.stop)

    p1 = positions[limb]
    traj.add_point(p1, 1.0)
    traj.add_point([s0, s1, e0, e1,  w0, w1,  w2], 1.0)
    traj.start()
    traj.wait(1.0)
    traj.clear(limb)
    timeout = time.time() + 60 *10 #Time to exit 
    while True:
        s0 = ref.ref[ha.LSY];
        s1 = ref.ref[ha.LSP];
        e0 = ref.ref[ha.LSR];
        e1 = ref.ref[ha.LEB] + 1.8;
        w0 = ref.ref[ha.LHY];
        w1 = ref.ref[ha.LHP];
        w2 = ref.ref[ha.LWR];
        #print "Time Remaining: %f. \nCurrent trajectory: s0 = %f, s1 = %f, e0 = %f, e1 = %f, w0 = %f, w1 = %f, w2 = %f" %((timeout -time.time()), ref.ref[ha.LSY], ref.ref[ha.LSP], ref.ref[ha.LSR], ref.ref[ha.LEB], ref.ref[ha.LHY], ref.ref[ha.LHP], ref.ref[ha.LWR])
        traj.add_point([s0, s1, e0, e1,  w0, w1,  w2], 0.01) #'0.01' executes trajectory in 0.01 seconds
        traj.start()
        traj.wait(1.0)
        traj.clear(limb)
        if time.time() > timeout:
            print "Time out. Quiting."
            break
        r.get(ref)
        #time.sleep(0.02) #not necessary because of 0.01 above

    print("Exiting - Joint Trajectory Action Test Complete")

if __name__ == "__main__":
    main()
