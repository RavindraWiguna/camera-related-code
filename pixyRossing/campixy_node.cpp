//
// begin license header
//
// This file is part of Pixy CMUcam5 or "Pixy" for short
//
// All Pixy source code is provided under the terms of the
// GNU General Public License v2 (http://www.gnu.org/licenses/gpl-2.0.html).
// Those wishing to use Pixy source code, software and/or
// technologies under different licensing terms should contact us at
// cmucam@cs.cmu.edu. Such licensing terms are available for
// all portions of the Pixy codebase presented here.
//
// end license header
//

#include <signal.h>
//emang ada error ini unless u change in vscode
#include "libpixyusb2.h"
#include <ros/ros.h>
#include <std_msgs/UInt8.h>
#include <std_msgs/UInt16MultiArray.h>
#include <stdint.h>


Pixy2        pixy;
static bool  run_flag = true;
std_msgs::UInt8 num;
std_msgs::UInt16MultiArray sig_x_y;


void handle_SIGINT(int unused)
{
  // On CTRL+C - abort! //
  //siap bosku
  run_flag = false;
}

int main(int argc, char **argv)
{
  int  Result;

  //=================================================ROS=================================
  ros::init(argc, argv, "campixy_node");
  ros::NodeHandle nh;
  ros::Publisher numBlocks_pub = nh.advertise<std_msgs::UInt8>
    ("pixyCam/numBlocks", 10);
  ros::Publisher sig_x_y_pub = nh.advertise<std_msgs::UInt16MultiArray>
    ("pixyCam/sig_x_y", 10);
  sig_x_y.data.push_back((uint16_t)0);
  sig_x_y.data.push_back((uint16_t)0);
  sig_x_y.data.push_back((uint16_t)0);
  //Dim is useless
  //=================================================ROS=================================

  // Catch CTRL+C (SIGINT) signals //
  signal (SIGINT, handle_SIGINT);

  printf ("=============================================================\n");
  printf ("= PIXY2 Get Blocks Demo                                     =\n");
  printf ("=============================================================\n");

  printf ("Connecting to Pixy2...");

  // Initialize Pixy2 Connection //
  {
    Result = pixy.init();

    if (Result < 0)
    {
      printf ("Error\n");
      printf ("pixy.init() returned %d\n", Result);
      return Result;
    }

    printf ("Success\n");
  }

  // Get Pixy2 Version information //
  {
    Result = pixy.getVersion();

    if (Result < 0)
    {
      printf ("pixy.getVersion() returned %d\n", Result);
      return Result;
    }

    pixy.version->print();
  }

  // Set Pixy2 to color connected components program //
  pixy.changeProg("color_connected_components");
  
  ros::Rate rate(32);

  while(ros::ok()){
    int Block_Index;

    // Query Pixy for blocks //
    pixy.ccc.getBlocks();

    // Were blocks detected? //
    if (pixy.ccc.numBlocks){
      // Blocks detected - print them! //
      num.data = pixy.ccc.numBlocks;
      // printf("Detected %d block(s)\n", pixy.ccc.numBlocks);
    
    
      for (Block_Index = 0; Block_Index < pixy.ccc.numBlocks; ++Block_Index){
        // printf ("  Block %d: ", Block_Index + 1);
        // pixy.ccc.blocks[Block_Index].print();

        sig_x_y.data[0] =  pixy.ccc.blocks[Block_Index].m_signature;
        sig_x_y.data[1] =  pixy.ccc.blocks[Block_Index].m_x;
        sig_x_y.data[2] =  pixy.ccc.blocks[Block_Index].m_y;

        sig_x_y_pub.publish(sig_x_y);

      }
    }
    numBlocks_pub.publish(num);
    

    if (run_flag == false){
      // Exit program loop //
      break;
    }
    ros::spinOnce();
    rate.sleep();
  }

  printf ("PIXY2 Get Blocks Demo Exit\n");
}
