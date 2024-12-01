import os

#summary_plot

summary_plot_dir=f'data\\template\\summary_plot'

#thing_card
thing_card_dir=f'data\\template\\thing_card'

#talk
talk_dir=f'data\\template\\talk'


TEMPLATE_DIRS={
    'summary_plot':summary_plot_dir,
    'thing_card':thing_card_dir,
    'talk':talk_dir
}


USER_NAME='user.txt'
AI_NAME='ai.txt'


def read_template(role,func_name):
    path=os.path.join(TEMPLATE_DIRS[f'{func_name}'],USER_NAME).replace('\\','/')
    with open(path, 'r', encoding='utf-8') as f:
        role['template']['user'] = f.read()

    path=os.path.join(TEMPLATE_DIRS[f'{func_name}'],AI_NAME).replace('\\','/')
    with open(path, 'r', encoding='utf-8') as f:
        role['template']['assistant'] = f.read()

    return role


