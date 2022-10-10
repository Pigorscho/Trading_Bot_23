from time import sleep

from scripts import win_taskbar_handler
from scripts.setup_handler import open_web_app, login, get_fut_stats, kill_browser
from scripts.scraping_handler import get_player_data
from scripts.web_app_handler import attempt_30_players, navigate, clear_transfer_list
from scripts.trading_number_storage_handler import TradingNumberStorage


def main_thread():
    print('hiding win taskbar')
    win_taskbar_handler.hide()
    print('starting Trading Bot ...')
    trading_number_storage_handle = TradingNumberStorage()
    no_result_counter = 0
    no_player_name_found = None
    open_web_app()
    print('logging in ...')
    while True:

        try:
            if not login():
                raise Exception('we fucked up the login :/')
            else:
                print('gathering Player Data ...')
                for page in range(8):
                    # big_num, small1, small2, tiny = get_fut_stats(trading_number_storage_handle)

                    # print('big', big_num)
                    # print('small1', small1)
                    # print('small2', small2)
                    # print('tiny', tiny)
                    attempt_30_players(trading_number_storage_handle, page, no_result_counter, no_player_name_found)


                '''
                        navigate('transfer_list')
                        # clear_transfer_list()
                        # -> use data for attempt_30_players(player_data -> max iterations until transfer_list is full
                        '''

                print('finished successful Trading!')
                # maybe pause due to botty or restart {amount}attempt_30_players(player)
        except Exception as e:
            print(f'main thread catched {e}\n-> restarting the whole bitch')
            kill_browser()
            open_web_app()

