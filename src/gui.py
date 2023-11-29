
import asyncio
from enum import Enum, auto
from itertools import chain


import logging
import queue
import justpy as jp
# FOR FUTURE PROJECTS: check out the justpy.react functionality: https://justpy.io/blog/reactivity/


import unified_planning as up
from unified_planning.shortcuts import *
from unified_planning.plot import plot_time_triggered_plan
from unified_planning.engines import ValidationResultStatus


GRAPH_IMAGE_LOCATION = "/logos/generated/graph"
GRAPH_IMAGE_DIMENSIONS = "height: 100%; width: 100%;"

FIGSIZE = 16, 11

MAX_ACTIONS = 15

WORD = "demo"
ADDITIONAL_WORDS = ["t", "table"]


class Mode(Enum):
    GENERATING_PROBLEM = auto()
    OPERATING = auto()


class Gui():
    def __init__(self):
        # a queue where the interface waits the start
        self.start_queue = queue.Queue()

        self.logger = logging.getLogger(__name__)
        logging.basicConfig(format='%(asctime)s %(message)s')
        self.logger.setLevel(logging.INFO)

        self.mode = Mode.GENERATING_PROBLEM

        self.plan = None
        self.plan_expected: bool = False
        self.image_id = 0

        self.generate_problem()

        self.plan_div: Optional[jp.Div] = None
        self.graph_image_div: Optional[jp.Img] = None

        self.jp_components = []
        from main_page import TEXT_INPUT_P_CLASS, TEXT_INPUT_P_STYLE
        for i in range(1, MAX_ACTIONS+1):
            input_txt_1 = jp.Input(
                classes=TEXT_INPUT_P_CLASS,
                style=TEXT_INPUT_P_STYLE,
                placeholder=f"Block"
            )
            input_txt_2 = jp.Input(
                classes=TEXT_INPUT_P_CLASS,
                style=TEXT_INPUT_P_STYLE,
                placeholder=f"Block or Table"
            )
            input_txt_3 = jp.Input(
                classes=TEXT_INPUT_P_CLASS,
                style=TEXT_INPUT_P_STYLE,
                placeholder=f"Block or Table"
            )
            self.jp_components.append((input_txt_1, input_txt_2, input_txt_3))

    def display_graph(self):
        if self.graph_image_div is None:
            return

        if self.plan is None:
            return

        img_loc = f"{GRAPH_IMAGE_LOCATION}_{self.image_id}.png"
        self.image_id += 1

        plot_time_triggered_plan(
            self.plan,
            filename = f".{img_loc}",
            figsize=FIGSIZE,
        )

        self.graph_image_div.delete_components()

        _ = jp.Img(
            a=self.graph_image_div,
            src=f"static{img_loc}",
            #style='max-width: 100%; height: 100%;'
            style = GRAPH_IMAGE_DIMENSIONS
        )

    def reset_execution(self):
        self.components_disabled(False)
        self.mode = Mode.GENERATING_PROBLEM

    def update_planning_execution(self):
        from main_page import PLAN_PART_P_CLASS, PLAN_PART_P_STYLE
        if self.plan_div is not None:
            self.plan_div.delete_components()
            if self.plan is not None and self.plan.status == ValidationResultStatus.INVALID:
                _ = jp.P(
                    a=self.plan_div,
                    text=f"The given plan is NOT VALID!",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
                _ = jp.P(
                    a=self.plan_div,
                    text=f"The reason is: {' '.join((lm.message for lm in self.plan.log_messages))}",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
            elif self.plan is not None and self.plan.status == ValidationResultStatus.VALID:
                _ = jp.P(
                    a=self.plan_div,
                    text=f"The given plan is VALID!",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
            elif self.plan_expected:
                if self.mode == Mode.GENERATING_PROBLEM:
                    single_p = jp.P(
                        a=self.plan_div,
                        text="Error!",
                        classes=PLAN_PART_P_CLASS,
                        style=PLAN_PART_P_STYLE,
                    )
                else:
                    single_p = jp.P(
                        a=self.plan_div,
                        text="Wait for validation to finish!",
                        classes=PLAN_PART_P_CLASS,
                        style=PLAN_PART_P_STYLE,
                    )
            else:
                single_p = jp.P(
                    a=self.plan_div,
                    text="Make a plan and press VALIDATE!",
                    classes=PLAN_PART_P_CLASS,
                    style=PLAN_PART_P_STYLE,
                )
            try:
                asyncio.run(self.plan_div.update())
            except RuntimeError:
                self.plan_div.update()
            self.display_graph()

    def clear_activities_click(self, msg):
        self.logger.info("Clearing")
        if self.mode == Mode.GENERATING_PROBLEM:
            for i_1, i_2, i_3 in self.jp_components:
                i_1.value = ""
                i_1.placeholder = "Block"
                i_2.value = ""
                i_2.placeholder = "Block or Table"
                i_3.value = ""
                i_3.placeholder = "Block or Table"

            self.plan_expected = False
            self.display_graph(True)
            self.update_planning_execution()

    def show_gui_thread(self):
        from main_page import main_page
        @jp.SetRoute("/")
        def get_main_page():
            return main_page(self)
        jp.justpy(get_main_page)

    def generate_problem_click(self, msg):
        self.logger.info("Generating")
        if self.mode == Mode.GENERATING_PROBLEM:
            self.mode = Mode.OPERATING
            self.components_disabled(True)
            if self.validate_input():
                self.logger.info("Valid input")
                self.plan = None
                self.plan_expected = True
                self.update_planning_execution()
                # unlock the planing method with the problem correctly generated
                self.start_queue.put(None)
            else:
                self.logger.info("Invalid input")
                self.mode = Mode.GENERATING_PROBLEM
                self.input_values = []
                self.components_disabled(False)

    def components_disabled(self, disabled: bool):
        for c in chain(*self.jp_components):
            c.disabled = disabled

    def validate_input(self) -> bool:
        self.input_values = []
        input_values = []
        if self.jp_components is None:
            return False
        finished = False
        for obj_jp, from_jp, to_jp in self.jp_components:
            obj_txt = obj_jp.value
            from_txt = from_jp.value
            to_txt = to_jp.value
            if finished:
                break
                if obj_txt:
                    obj_jp.value = "Err: Empty action(s) above"
                if from_txt:
                    from_jp.value = "Err: Empty action(s) above"
                if to_jp:
                    from_jp.value = "Err: Empty action(s) above"
                return False
            else:
                obj = self.objects_mapping.get(obj_txt.lower(), None)
                if obj is None:
                    if obj_txt:
                        obj_jp.value = f"Err: {obj_txt} Not found"
                        return False
                    else:
                        finished = True
                        break
                elif obj == self.objects_mapping.get("table"):
                    obj_jp.value = f"Err: table"
                    return False
                from_obj = self.objects_mapping.get(from_txt.lower(), None)
                if from_obj is None:
                    if not finished and from_txt:
                        from_jp.value = f"Err: {from_txt} Not found"
                        return False
                    elif not finished:
                        from_jp.value = f"Err: Block non specified"
                        return False
                to_obj = self.objects_mapping.get(to_txt.lower(), None)
                if to_obj is None:
                    if not finished and to_txt:
                        to_jp.value = f"Err: {to_txt} Not found"
                        return False
                    elif not finished:
                        to_jp.value = f"Err: Block non specified"
                        return False
                input_values.append((obj, from_obj, to_obj))
        self.input_values = input_values
        return True

    def generate_problem(self):

        self.logger.info("Generating planning problem...")


        Entity = UserType("Entity", None)  # None can be avoided
        Location = UserType("Location", Entity)
        Unmovable = UserType("Unmovable", Location)
        TableSpace = UserType("TableSpace", Unmovable)
        Movable = UserType("Movable", Location)
        Block = UserType("Block", Movable)
        clear = Fluent("clear", BoolType(), space=Location)
        on = Fluent("on", BoolType(), object=Movable, space=Location)
        # hierarchical blocks world
        problem = Problem("hierarchical_blocks_world")
        table = problem.add_object("table", TableSpace)
        objects_mapping = {
            "t": table,
            "table": table,
        }

        move = InstantaneousAction("move", item=Movable, l_from=Location, l_to=Location)
        item = move.parameter("item")
        l_from = move.parameter("l_from")
        l_to = move.parameter("l_to")
        move.add_precondition(clear(item))
        move.add_precondition(clear(l_to))
        move.add_precondition(on(item, l_from))
        move.add_effect(clear(l_from), True)
        move.add_effect(on(item, l_from), False)
        move.add_effect(clear(l_to), False, Not(Equals(l_to, table)))
        move.add_effect(on(item, l_to), True)

        problem.add_fluent(clear, default_initial_value=True)
        problem.add_fluent(on, default_initial_value=False)
        problem.add_action(move)
        prev_element = table
        for w in reversed(WORD.lower()):
            obj = problem.add_object(w, Block)
            objects_mapping[w] = obj
            problem.set_initial_value(on(obj, table), True)
            problem.add_goal(on(obj, prev_element))
            prev_element = obj

        # The blocks are all on ts_1, in order block_3 under block_1 under block_2

        self.problem = problem
        self.objects_mapping = objects_mapping


def write_action_instance(action_instance: up.plans.ActionInstance) -> str:
    return str(action_instance)

async def reload_page():
    for page in jp.WebPage.instances.values():
        if page.page_type == 'main':
            await page.reload()
