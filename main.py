import argparse
from utils import DictTree
import agents
import envs
import pickle
import time
import robo_ani
import plot
import sys


def rollout(config):
    env = envs.catalog(DictTree(
        domain_name=config.domain,
        hardware_name=config.hardware
    ))
    agent = agents.catalog(DictTree(
        domain_name=config.domain,
        task_name=config.task,
        rollable=True,
        model_dirname=config.model,
        hardware_name=config.hardware,
        evaluation=config.eval
    ))

    init_arg = env.reset()
    agent.reset(init_arg)
    trace = agent.rollout(env)
    time_stamp = time.strftime("%Y-%m-%d %H-%M-%S", time.gmtime())
    # pickle.dump(trace, open("{}/{}/{}/{}.pkl".format(config.data, config.domain, config.task,  time_stamp), 'wb'),
    #             protocol=2)
    pickle.dump(trace, open(f"{config.data}/{config.domain}/{config.task}/trace_result_{time_stamp}.pkl", 'wb'),
                protocol=2)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--domain')
    parser.add_argument('--task')
    parser.add_argument('--model')
    parser.add_argument('--data')
    parser.add_argument('--hardware')
    parser.add_argument('--eval')
    args = parser.parse_args()

    # for i in range(20):
    rollout(args)
    # time.sleep(5)

    # Displays GUI of robot moving through gridworld

    moves_list = pickle.load(open("moves_list.pkl", 'rb'))
    robo_ani.display_env(args.hardware, moves_list)

    # Creates video of hierarchy

    # plot.make_hierarchy_video("trace_result.pkl", "plot_output_robot.mp4")
    # plot.make_hierarchy_video("trace_result.pkl", "./plot_out.avi")
