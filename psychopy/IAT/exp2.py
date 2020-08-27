
# Date: 2020-01-04

from psychopy import visual, core, event
from psychopy.visual import ShapeStim
from psychopy import gui
from psychopy import logging
import random
import sys
import pandas as pd


# function for get agent's response,reaction time and correct
def get_button(trial, inverse=False):
    # reset the clock
    respClock.reset()
    keys = event.waitKeys(keyList=['f', 'j', 'escape'])
    rt = respClock.getTime()
    if trial < 10 and keys == ['f']:
        correct = 1
    elif trial > 10 and keys == ['j']:
        correct = 1
    else:
        correct = 0
    if keys == ['escape']:
        win.close()
    # inverse argument for phase 5 and phase 6/7
    if inverse == True:
        correct = 1 if correct == 0 else 0
    return keys, rt, correct


# function for combining the face picture index and hint word index into lists
def combine_pic_word(block):
    # filter the index
    good_word_index = [k for k, v in word_dic.items() if k < 10]
    bad_word_index = [k for k, v in word_dic.items() if k > 10]
    light_makeup_index = [k for k, v in pic_dic.items() if k < 10]
    heavy_makeup_index = [k for k, v in pic_dic.items() if k > 10]
    combine1, combine2 = [], []
    # combine the index
    if block == 3 or block == 4:
        for a in light_makeup_index:
            for b in good_word_index:
                e = [b, a]
                combine1.append(e)

        for c in heavy_makeup_index:
            for d in bad_word_index:
                f = [d, c]
                combine2.append(f)
    elif block == 6 or block == 7:
        for a in heavy_makeup_index:
            for b in good_word_index:
                e = [b, a]
                combine1.append(e)

        for c in light_makeup_index:
            for d in bad_word_index:
                f = [d, c]
                combine2.append(f)

    combine_trial = combine2 + combine1
    # shuffle the index
    random.shuffle(combine_trial)
    return combine_trial


def phase_1_2_5(trial_set, loop=2, block=1):
    win.flip()
    trial_number, a, sequence = trial_set, 0, 1
    #list for storaging the data
    sequence_list, rt_list, button_list, correct_list, stim_num_list, stim_type_list, block_list = [], [], [], [], [], [], []
    for n in range(0, loop):
        random.shuffle(trial_number)
        for trial in trial_number:

            stim_num_list.append(trial)
            sequence_list.append(sequence)
            block_list.append(block)
            #updathe the stim index
            if block==2:
                word.text = word_dic[trial]
            face_pic.image = pic_dic[trial]

            if block == 1 or block == 5:
                face_pic.draw()
                if block ==1:
                    guide_pic_1_left.draw()
                    guide_pic_1_right.draw()
                elif block==5:
                    guide_pic_2_left.draw()
                    guide_pic_2_right.draw()
                stim_type_list.append('face picture')
            elif block == 2:
                word.draw()
                guide_word_left.draw()
                guide_word_right.draw()
                stim_type_list.append('hint word')
            win.flip()
            trial_infor = get_button(trial, inverse=True) if block == 5 else get_button(trial, inverse=False)
            key, rt, correct = trial_infor[0], trial_infor[1], trial_infor[2]
            button_list.append(key)
            rt_list.append(rt)
            correct_list.append(correct)
            #specific trial for wrong trials in practice phase
            while correct == 0:
                sequence_list.append(sequence)
                block_list.append(block)
                stim_num_list.append(trial)

                if block == 1 or block == 5:
                    face_pic.draw()
                    if block == 1:
                        guide_pic_1_left.draw()
                        guide_pic_1_right.draw()
                    elif block == 5:
                        guide_pic_2_left.draw()
                        guide_pic_2_right.draw()
                    stim_type_list.append('face picture')
                elif block == 2:
                    word.draw()
                    guide_word_left.draw()
                    guide_word_right.draw()
                    stim_type_list.append('hint word')
                wrong_msg.draw()
                win.flip()
                trial_infor = get_button(trial, inverse=True) if block == 5 else get_button(trial, inverse=False)
                key, rt, correct = trial_infor[0], trial_infor[1], trial_infor[2]
                button_list.append(key)
                rt_list.append(rt)
                correct_list.append(correct)
            #trial sequence plus 1
            sequence += 1
    return sequence_list, rt_list, button_list, correct_list, stim_num_list, stim_type_list, block_list


def phase_3_4_6_7(block=3):
    win.flip()
    trial_set = combine_pic_word(block=block)
    sequence, sequence_list, rt_list, button_list, correct_list, stim_num_list, stim_type_list, block_list = 1, [], [], [], [], [], [], []
    for trial in trial_set:

        sequence_list.append(sequence)
        block_list.append(block)

        stim_num_list.append(trial[0])
        word.text = word_dic[trial[0]]
        face_pic.image = pic_dic[trial[1]]

        word.draw()
        stim_type_list.append('hint word')
        if block == 3 or block == 4:
            guide_1_left.draw()
            guide_1_right.draw()
        else:
            guide_2_left.draw()
            guide_2_right.draw()
        win.flip()
        trial_infor = get_button(trial[0], inverse=False)
        key, rt, correct = trial_infor[0], trial_infor[1], trial_infor[2]
        button_list.append(key)
        rt_list.append(rt)
        correct_list.append(correct)
        while correct == 0 and (block == 3 or block == 6):
            sequence_list.append(sequence)
            block_list.append(block)
            stim_num_list.append(trial[0])
            stim_type_list.append('hint word')

            wrong_msg.draw()
            word.draw()
            if block == 3 or block == 4:
                guide_1_left.draw()
                guide_1_right.draw()
            else:
                guide_2_left.draw()
                guide_2_right.draw()
            win.flip()
            trial_infor = get_button(trial[0], inverse=False)
            key, rt, correct = trial_infor[0], trial_infor[1], trial_infor[2]
            button_list.append(key)
            rt_list.append(rt)
            correct_list.append(correct)
        
        sequence_list.append(sequence)
        block_list.append(block)
        stim_num_list.append(trial[1])
        stim_type_list.append('face picture')
        face_pic.draw()
        if block == 3 or block == 4:
            guide_1_left.draw()
            guide_1_right.draw()
        else:
            guide_2_left.draw()
            guide_2_right.draw()

        win.flip()
        trial_infor = get_button(trial[1], inverse=False) if block == 3 or block == 4 else get_button(trial[1],
                                                                                                      inverse=True)
        key, rt, correct = trial_infor[0], trial_infor[1], trial_infor[2]
        button_list.append(key)
        rt_list.append(rt)
        correct_list.append(correct)
        while correct == 0 and (block == 3 or block == 6):
            sequence_list.append(sequence)
            block_list.append(block)
            stim_num_list.append(trial[1])
            stim_type_list.append('face picture')

            wrong_msg.draw()
            face_pic.draw()
            if block == 3 or block == 4:
                guide_1_left.draw()
                guide_1_right.draw()
            else:
                guide_2_left.draw()
                guide_2_right.draw()
            win.flip()
            trial_infor = get_button(trial[1], inverse=False) if block == 3 or block == 4 else get_button(trial[1],
                                                                                                          inverse=True)
            key, rt, correct = trial_infor[0], trial_infor[1], trial_infor[2]
            button_list.append(key)
            rt_list.append(rt)
            correct_list.append(correct)

        sequence += 1
    return sequence_list, rt_list, button_list, correct_list, stim_num_list, stim_type_list, block_list


if __name__ == '__main__':
    # create a DlgFromDict
    inf = {'user': 'sub ', 'name': '1', 'age': '19', 'gender': ['M', 'F']}
    dlg = gui.DlgFromDict(dictionary=inf, title='被试信息', order=['user', 'age', 'gender'])
    if not dlg.OK:
        core.quit()
    filename = ('data\{user}'.format(**inf))

    # add logfile
    logfile = logging.LogFile(filename + ".log",
                              filemode='w',
                              level=logging.EXP)

    # set window and ratingscale
    win = visual.Window([1024, 768], units='height', color='white', fullscr=False)

    # set up word and face picture dictionary
    word_dic = {1: u'能力高', 11: u'能力低', 2: u'信任', 12: u'不信任', 3: '道德高', 13: u'道德低', 4: '心理健康', 14: '心理不健康'}
    pic_dic = {1: u'L-2.jpg', 11: u'H-2.jpg', 2: u'L-7.jpg', 12: u'H-7.jpg', 3: 'L-8.jpg', 13: u'H-8.jpg',
               4: u'L-16.jpg',
               14: u'H-16.jpg', 5: u'L-22.jpg', 15: u'H-22.jpg'}

    # initialize stim and picture
    wrong_msg = visual.TextStim(win, text='X', pos=(0.0, -0.4), color='red', bold=True, height=0.06)
    rest_msg = visual.TextStim(win, height=0.1,text='休息完毕后请按空格开始',color='black',bold=True)
    thankword = visual.TextStim(win, text='谢谢参与', pos=(0.0, 0.0), color='black', bold=True)
    word = visual.TextStim(win, text='', pos=(0.0, 0.0), color='black', bold=True)
    face_pic = visual.ImageStim(win, image='L-2.jpg', size=0.66, pos=(0.0, 0.0))
    instruction1 = visual.ImageStim(win, image='instruction1.png')
    instruction2 = visual.ImageStim(win, image='instruction2.png')
    instruction3 = visual.ImageStim(win, image='instruction3.png')
    instruction5 = visual.ImageStim(win, image='instruction5.png')
    instruction6 = visual.ImageStim(win, image='instruction6.png')

    guide_1_left = visual.ImageStim(win, image='guide_1_left.png', size=0.2, pos=(-0.8, 0.4))
    guide_1_right = visual.ImageStim(win, image='guide_1_right.png', size=0.2, pos=(0.8, 0.4))
    guide_2_left = visual.ImageStim(win, image='guide_2_left.png', size=0.2, pos=(-0.8, 0.4))
    guide_2_right = visual.ImageStim(win, image='guide_2_right.png', size=0.2, pos=(0.8, 0.4))

    guide_pic_1_left=visual.ImageStim(win, image='淡妆.png', size=0.2, pos=(-0.8, 0.4))
    guide_pic_1_right=visual.ImageStim(win, image='浓妆.png', size=0.2, pos=(0.8, 0.4))
    guide_pic_2_left = visual.ImageStim(win, image='淡妆.png', size=0.2, pos=(-0.8, 0.4))
    guide_pic_2_right = visual.ImageStim(win, image='浓妆.png', size=0.2, pos=(0.8, 0.4))
    guide_word_left=visual.ImageStim(win, image='积极词.png', size=0.2, pos=(-0.8, 0.4))
    guide_word_right=visual.ImageStim(win, image='消极词.png', size=0.2, pos=(0.8, 0.4))
    

    # set the clock for timing
    respClock = core.Clock()

    # set the trial set for phase1 ,phase2 and phase5
    word_trial = [1, 11, 2, 12, 3, 13, 4, 14]
    pic_trial = [1, 11, 2, 12, 3, 13, 4, 14, 5, 15]

    # proceed the task
    instruction1.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    first_phase = phase_1_2_5(trial_set=pic_trial, block=1)
    rest_msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    instruction2.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    second_phase = phase_1_2_5(trial_set=word_trial, block=2)
    rest_msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    instruction3.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    third_phase = phase_3_4_6_7(block=3)
    rest_msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    instruction3.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    fourth_phase = phase_3_4_6_7(block=4)
    rest_msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    instruction5.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    fifth_phase = phase_1_2_5(trial_set=pic_trial, block=5)
    rest_msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    instruction6.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    sixth_phase = phase_3_4_6_7(block=6)
    rest_msg.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    instruction6.draw()
    win.flip()
    keys = event.waitKeys(keyList=['space'])
    seventh_phase = phase_3_4_6_7(block=7)

    #combine the data from different phase
    trial_sequence = first_phase[0]+second_phase[0]+third_phase[0]+fourth_phase[0]+fifth_phase[0]+sixth_phase[0]+seventh_phase[0]
    reaction_time = first_phase[1]+second_phase[1]+third_phase[1]+fourth_phase[1]+fifth_phase[1]+sixth_phase[1]+seventh_phase[1]
    button_press = first_phase[2]+second_phase[2]+third_phase[2]+fourth_phase[2]+fifth_phase[2]+sixth_phase[2]+seventh_phase[2]
    right = first_phase[3]+second_phase[3]+third_phase[3]+fourth_phase[3]+fifth_phase[3]+sixth_phase[3]+seventh_phase[3]
    stim_index = first_phase[4]+second_phase[4]+third_phase[4]+fourth_phase[4]+fifth_phase[4]+sixth_phase[4]+seventh_phase[4]
    stim_type = first_phase[5]+second_phase[5]+third_phase[5]+fourth_phase[5]+fifth_phase[5]+sixth_phase[5]+seventh_phase[5]
    block = first_phase[6]+second_phase[6]+third_phase[6]+fourth_phase[6]+fifth_phase[6]+sixth_phase[6]+seventh_phase[6]

    #transfer data list to dataframe
    df = pd.DataFrame([trial_sequence, reaction_time, button_press, right,stim_index,stim_type,block])
    df = df.T
    df.columns = 'trial_sequence', 'reaction time', 'pressed button', 'correct','stim index','stim type','block'

    user_df, age_df, name_df, gender_df = pd.DataFrame([inf['user']], columns=['subject number']), pd.DataFrame([inf['age']], columns=['age']), pd.DataFrame(
        [inf['name']], columns=['subject name']), pd.DataFrame([inf['gender']], columns=['gender'])
    df = pd.concat([df, user_df, age_df, name_df, gender_df], axis=1)
    df = df.fillna(method='ffill')

    #write to csv file
    df.to_csv(filename+'.csv',mode='a',header=True,index=False)

    #the end of task
    thankword.draw()
    win.flip()
    core.wait(2)
    win.close()


