import networkx as nx
from typing import Tuple
from up_graphene_engine.engine import  GrapheneEngine
from gui import Gui, WORD

from unified_planning.shortcuts import *
from unified_planning.plans import ActionInstance, SequentialPlan
import unified_planning as up
import unified_planning.engines
import unified_planning.model
import unified_planning.model.metrics

get_environment().credits_stream = None


def planning(engine: GrapheneEngine, gui: Gui, reload_page):
    gui.logger.info("Parsing plan...")

    problem = gui.problem

    def generate_action_instance(obj_from_to) -> ActionInstance:
        return ActionInstance(problem.action("move"), obj_from_to)

    plan = SequentialPlan(list(map(generate_action_instance, gui.input_values)))
    gui.logger.info(f"Plan created: {plan}")
    gui.logger.info(f"Sending request")

    res = engine.validate(problem, plan)

    return res
