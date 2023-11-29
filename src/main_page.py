from functools import partial
import re

import justpy as jp

from gui import Gui, Mode, MAX_ACTIONS

LEFT_MARGIN, RIGHT_MARGIN = " margin-left: 10px; ", " margin-right: 20px; "

TITLE_DIV_CLASS = "grid justify-between gap-2 grid-cols-3"
TITLE_DIV_STYLE = "grid-template-columns: auto auto auto; margin-top: 15px;" + LEFT_MARGIN + RIGHT_MARGIN

TITLE_TEXT_DIV_STYLE = "font-size: 80px; text-align: center; text-weight: bold;"

DESCRIPTION_STYLE = "margin-top: 15px; font-size: 16px;" + LEFT_MARGIN + RIGHT_MARGIN
DESCRIPTION_TEXT = """
Validation demo: in this demo you can specify a plan; using the "move" action you can make a plan to move blocks around.
In the beginning all blocks are on the table (as in the figure) and the required final state for a valid plan is to have the "demo" word created (as the figure shows).
Using the input text you can instantiate "move" actions to move the blocks around.
To move a block there are some restrictions:
 1: The block must be clear (no blocks above it).
 2: The block must be on the block/table it is required to be moved from.
 3: If the destination of the block is another block, the other block must be clear.
Not respecting any of these conditions will automatically set the plan as invalid.
If a "legal" plan is submitted, it is invalid if it does not reach the required configuration.
"""
SINGLE_DESCRIPTION_STYLE = LEFT_MARGIN + RIGHT_MARGIN


MAIN_BODY_DIV_CLASS = "grid grid-cols-3 gap-7"
MAIN_BODY_DIV_STYLE = "grid-template-columns: max-content max-content max-content; column-gap: 15px; margin-top: 15px;" + LEFT_MARGIN + RIGHT_MARGIN

ACTIONS_DIV_CLASS = "grid"
# Setting height to 0 it'sa trick to solve the problem of the goal div changing size
ACTIONS_DIV_STYLE = f"grid-template-columns: max-content auto; font-size: 30px; font-weight: semibold; height: 0px;"

# INPUT_DESCRIPTION_P_CLASS = ""
# INPUT_DESCRIPTION_P_STYLE = "font-size: 16px; font-weight: normal; margin-top: 10px;"


ADD_BUTTON_CLASS = "bg-transparent hover:bg-blue-500 text-blue-700 font-semibold hover:text-white py-2 px-4 border border-blue-500 hover:border-transparent rounded m-2"
ADD_BUTTON_STYLE = f"font-weight: semibold; font-size: 20px; width: 150px; margin-top: 5px;"

GOALS_DIV_CLASS = ""
GOALS_DIV_STYLE = "font-size: 30px; font-weight: semibold; height: 0px;"

TEXT_WIDTH = 100 # px
COLUMN_GAP = 4 # px
box_width = 4*TEXT_WIDTH + 3*COLUMN_GAP
GOALS_CONTAINER_INPUT_CLASS = "grid"
# GOALS_CONTAINER_INPUT_STYLE = f"grid-template-columns: fit-content fit-content fit-content fit-content; font-weight: normal; font-size: 18px; column-gap: 4px;"
GOALS_CONTAINER_INPUT_STYLE = f"grid-template-columns: {TEXT_WIDTH}px {TEXT_WIDTH}px {TEXT_WIDTH}px {TEXT_WIDTH}px {TEXT_WIDTH}px {TEXT_WIDTH}px; font-weight: normal; font-size: 18px; column-gap: 4px;"

TXT = f"font-weight: normal; font-size: 16px; margin-top: 5px; width: {TEXT_WIDTH}px; "

DEFAULT_TEXT_P_CLASS = ""
DEFAULT_TEXT_P_STYLE = TXT

TEXT_INPUT_P_CLASS = ""
TEXT_INPUT_P_STYLE = f"{TXT}padding: 5px; background-color:  #e1eff7; border: 0.9px solid #000;"
# TEXT_INPUT_P_STYLE = f"font-weight: normal; font-size: 16px; border: 0.9px solid #000; background-color: #e1eff7; padding: 5px; width: {TEXT_WIDTH}px; margin-top: 5px;"

CLEAR_SOLVE_BUTTONS_DIV_CLASS = "flex grid-cols-2"
CLEAR_SOLVE_BUTTONS_DIV_STYLE = f"column-gap: 4px;"

CLEAR_SOLVE_BUTTONS_CLASS = ADD_BUTTON_CLASS
CLEAR_SOLVE_BUTTONS_STYLE = "font-weight: semibold; font-size: 20px;"

PLAN_DIV_CLASS = ""
PLAN_DIV_STYLE = f"font-size: 30px; font-weight: semibold;"

PLAN_PART_P_CLASS = ""
PLAN_PART_P_STYLE = f"font-weight: normal; font-size: 18px;"


def main_page(gui: Gui):
    wp = jp.WebPage(delete_flag = False)
    wp.page_type = 'main'
    title_div = jp.Div(
        a=wp,
        classes=TITLE_DIV_CLASS,
        style=TITLE_DIV_STYLE,
    )
    fbk_logo_div = jp.Div(
        a=title_div,
        # text="FBK LOGO",
        # style="font-size: 30px;",
        style="height: 160px;",
    )
    fbk_logo = jp.Img(
        src="/static/logos/fbk.png",
        a=fbk_logo_div,
        classes="w3-image",
        # style="height: 100%; length: auto;",
    )
    title_text_div = jp.Div(
        a=title_div,
        text="BLOCKS-WORLD",
        style=TITLE_TEXT_DIV_STYLE,
    )
    unified_planning_logo_div = jp.Div(
        a=title_div,
        style="height: 160px;",
    )
    unified_planning = jp.Img(
        src="/static/logos/unified_planning_logo.png",
        a=unified_planning_logo_div,
        classes="w3-image",
        style="max-width: 100%; height: 160px;"
    )

    description_div = jp.Div(
        a=wp,
        style=DESCRIPTION_STYLE,
    )
    for single_desc in DESCRIPTION_TEXT.split("\n"):
        description_paragraph = jp.P(
            a=description_div,
            style=SINGLE_DESCRIPTION_STYLE,
            text=single_desc,
        )

    main_body_div = jp.Div(
        a=wp,
        classes=MAIN_BODY_DIV_CLASS,
        style=MAIN_BODY_DIV_STYLE,
    )

    plan_div = jp.Div(
        a=main_body_div,
        classes=GOALS_DIV_CLASS,
        style=GOALS_DIV_STYLE,
        text="INPUT PLAN:"
    )

    plan_input_div = jp.Div(
        a=plan_div,
        classes=GOALS_CONTAINER_INPUT_CLASS,
        style=GOALS_CONTAINER_INPUT_STYLE,
    )

    # plan_inputs = []
    # for i in range(1, MAX_ACTIONS+1):
    #     _ = jp.Div(
    #         a=plan_input_div,
    #         text=f"{i}) Move",
    #         classes=DEFAULT_TEXT_P_CLASS,
    #         style=DEFAULT_TEXT_P_STYLE,
    #     )
    #     input_txt_1 = jp.Input(
    #         a=plan_input_div,
    #         classes=TEXT_INPUT_P_CLASS,
    #         style=TEXT_INPUT_P_STYLE,
    #         placeholder=f"Block"
    #     )
    #     _ = jp.Div(
    #         a=plan_input_div,
    #         text=f"FROM",
    #         classes=DEFAULT_TEXT_P_CLASS,
    #         style=DEFAULT_TEXT_P_STYLE,
    #     )
    #     input_txt_2 = jp.Input(
    #         a=plan_input_div,
    #         classes=TEXT_INPUT_P_CLASS,
    #         style=TEXT_INPUT_P_STYLE,
    #         placeholder=f"Block or Table"
    #     )
    #     _ = jp.Div(
    #         a=plan_input_div,
    #         text=f"TO",
    #         classes=DEFAULT_TEXT_P_CLASS,
    #         style=DEFAULT_TEXT_P_STYLE,
    #     )
    #     input_txt_3 = jp.Input(
    #         a=plan_input_div,
    #         classes=TEXT_INPUT_P_CLASS,
    #         style=TEXT_INPUT_P_STYLE,
    #         placeholder=f"Block or Table"
    #     )
    #     plan_inputs.append((input_txt_1, input_txt_2, input_txt_3))
    # gui.jp_components = plan_inputs

    for i, (i_1, i_2, i_3) in enumerate(gui.jp_components, 1):
        _ = jp.Div(
            a=plan_input_div,
            text=f"{i}) Move",
            classes=DEFAULT_TEXT_P_CLASS,
            style=DEFAULT_TEXT_P_STYLE,
        )
        plan_input_div.add_component(i_1)
        _ = jp.Div(
            a=plan_input_div,
            text=f"FROM",
            classes=DEFAULT_TEXT_P_CLASS,
            style=DEFAULT_TEXT_P_STYLE,
        )
        plan_input_div.add_component(i_2)
        _ = jp.Div(
            a=plan_input_div,
            text=f"TO",
            classes=DEFAULT_TEXT_P_CLASS,
            style=DEFAULT_TEXT_P_STYLE,
        )
        plan_input_div.add_component(i_3)

    reset_submit_buttons_div = jp.Div(
        a=plan_div,
        classes=CLEAR_SOLVE_BUTTONS_DIV_CLASS,
        style=CLEAR_SOLVE_BUTTONS_DIV_STYLE,
    )

    reset = jp.Input(
        a=reset_submit_buttons_div,
        value="RESET",
        type="submit",
        classes=ADD_BUTTON_CLASS,
        style=ADD_BUTTON_STYLE,
    )
    reset.on('click', gui.clear_activities_click)
    solve = jp.Input(
        a=reset_submit_buttons_div,
        value="VALIDATE",
        type="submit",
        classes=ADD_BUTTON_CLASS,
        style=ADD_BUTTON_STYLE,
    )
    solve.on('click', gui.generate_problem_click)

    problem_img_div = jp.Div(
        a=main_body_div,
        classes=GOALS_DIV_CLASS,
        style=GOALS_DIV_STYLE,
        text="PROBLEM IMAGE:",
    )

    problem_img = jp.Img(
        src="/static/logos/component_image.png",
        a=problem_img_div,
        classes="w3-image",
        style="max-width: 100%; height: 300px; border: 0.9px solid #000;",
    )

    plan_div = jp.Div(
        a=main_body_div,
        text="RESULT:",
        classes=PLAN_DIV_CLASS,
        style=PLAN_DIV_STYLE,
    )
    gui.plan_div = plan_div

    gui.update_planning_execution()

    return wp
