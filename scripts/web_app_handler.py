import clipboard
import pyautogui
from time import sleep

from scripts.utils import rtime
from scripts.pysin import locate, locate_consecutively, wait_for, rtype, wait_for_multiple
from scripts.setup_handler import open_web_app, login
from scripts.scraping_handler import PriceGatherer, get_player_data
from scripts.db_handler import DBHandler
from scripts.pause_handler import auto_pause, no_player_found_pause

black_list = [
    'Piero Hincapié',
    'Moise Kean',
    'Odriozola',
    'Amadou Haidara',
    'Mohamed Simakan'
]



def navigate(path):
    boolean = False
    nav_main_off = locate(r'pics\nav_main_off.png', reg=(8, 135, 126 - 8, 720 - 135))
    if nav_main_off:
        print('heading back to Main Menu ...')
        pyautogui.click(nav_main_off)
        rtime(2)

    if path == 'transfer_market':
        nav_transfers_off = locate(r'pics\nav_transfers_off.png', reg=(0, 350, 136 - 0, 464 - 350))
        if nav_transfers_off:
            print('clicking on Transfers Button ...')
            pyautogui.click(nav_transfers_off)
            rtime(1)
            nav_transfers_market = locate(r'pics\nav_transfers_market.png', reg=(870, 214, 1305 - 870, 300 - 214))
            if nav_transfers_market:
                print('heading in Transfers Market...')
                pyautogui.click(nav_transfers_market)
                rtime(1)
                print('ready to Trade // scraping Players Market Price ...')
                if wait_for(r'pics\nav_transfer_checkpoint.png', reg=(158, 117, 539 - 158, 195 - 117)):
                    print('Found Transfer Market Checkpoint !')
                    boolean = True
                    rtime(1)
    elif path == 'transfer_list':
        nav_transfers_off = locate(r'pics\nav_transfers_off.png', reg=(0, 350, 136 - 0, 464 - 350))
        if nav_transfers_off:  # , nav_transfers_market
            print('clicking on Transfers Button ...')
            pyautogui.click(nav_transfers_off)
            rtime(1)
            print('insert here auto number read ............')
            nav_transfers_list = locate(r'pics\nav_transfers_list.png', reg=(870, 578, 1140 - 870, 655 - 578))
            if nav_transfers_list:
                print('heading in Transfers List ...')
                pyautogui.click(nav_transfers_list)
                rtime(1)
                if wait_for(r'pics\nav_transfer_list_checkpoint.png', reg=(145, 127, 406 - 145, 190 - 127)):
                    print('Found Transfer List Checkpoint !')
                    boolean = True
                    rtime(1)
                # print('organizing Transfers List ...')
    else:
        raise Exception(f'it seems u misspelled {path}')
    return boolean


def attempt_30_players(trading_number_storage_handle, page, no_player_name_found, no_result_counter):  # ruf sich selbst auf wenn failsafe triggered
    if navigate('transfer_market'):
        for player30 in get_player_data(page):
            player_data = check_player_data(player30)
            for player in player_data:
                print(f'{player.__dict__ = }')
                enter_player_data(player, no_player_name_found)
                if no_player_name_found:
                    continue
                live_price = PriceGatherer(player.url).get_market_price()
                player.set_market_price(live_price)
                success = buy_player(player, trading_number_storage_handle, no_result_counter)
                if success: trading_number_storage_handle.increment_succ_purchase()
                if trading_number_storage_handle.succ_purchase == 100:
                    auto_pause()
                    return


def check_player_data(player_data_to_sanitize):
    # player_data = [player for player in player_data_to_sanitize if not DBHandler().is_listed(player.name)]
    player_data = []
    for player in player_data_to_sanitize:
        is_listed = DBHandler().is_listed(player.name)
        print(f'{player.name} is listed: {is_listed}')
        if not is_listed:
            player_data.append(player)
    length = len(player_data)
    if length == 0:
        print(f'out of these players i couldn\'t work so meesa is sleeping for a min:\n{player_data_to_sanitize}')
        no_player_found_pause()
    return player_data


def enter_player_data(player, no_player_name_found):
    clear_player_name_input_params = [
        {
            'id': 'cross', 'pic': r'pics\clear_player_name_input.png', 'to_appear': True,
            'to_disappear': False, 'reg': (1798, 364, 1898 - 1798, 440 - 364), 'con': .9
        },
        {
            'id': 'input', 'pic': r'pics\enter_player_name.png', 'to_appear': True,
            'to_disappear': False, 'reg': (794, 361, 1003 - 794, 434 - 361), 'con': .9
        }
    ]
    clear_player_name_input_multi = wait_for_multiple(clear_player_name_input_params, max_iterations=5, sleep_dur=1)
    if clear_player_name_input_multi.group():
        if clear_player_name_input_multi.hasattr('location'):
            id, location = clear_player_name_input_multi.group()
            # print('clicking on cross') if id == 'cross' else print('clicking into input field')
            pyautogui.click(location)
            rtime(1)

            if id == 'cross':
                # print('cleared previous Players Name ...')
                clear_player_name_input = wait_for(
                    r'pics\enter_player_name.png', reg=(794, 361, 1003 - 794, 434 - 361),
                    max_iterations=50, sleep_dur=.1
                )
                # print(f'{clear_player_name_input = }')
                if clear_player_name_input:
                    print('clicking on cross so I can enter player.name')
                    pyautogui.click(clear_player_name_input)
                    rtime(1)
            # print('writing Players Name ...')
            rtype(player.name, dur=.01 / 4)
            rtime(1.5)
            # print('selecting Player ...')
            """
            check if bad result xxxxxxxxxxxxxxxxx here
            """
            no_player_name = locate(r'pics\no_player_name', reg=(1202, 437, 1457 - 1202, 531 - 437))
            if no_player_name:
                print('Player does not exist / adding to bad_Player_List ...')

                return no_player_name



            pyautogui.click(867, 486)  # selecting first player
            rtime(1)
            # check if no results
            # if no_results = True
            # append player.data(blacklist[])
            delete_bid_filter = locate(
                r'pics\delete_buy_player_price.png', reg=(1751, 683, 1921 - 1751, 751 - 683))
            if delete_bid_filter:
                # print('deleting previous filter setting : "Bid Filter"')
                pyautogui.click(delete_bid_filter)
                rtime(1)
            delete_qual_and_rar = locate(r'pics\deselect_player_rarity.png', reg=(1227, 415, 1338 - 1227, 493 - 415))
            if delete_qual_and_rar:
                # print('deleting previous filter setting : "Quality and Rarity"')
                pyautogui.click(delete_qual_and_rar)
                rtime(0.75)

            """
            
            Hier muss die restleiche Data eingefügt werden
            
            """


def buy_player(player, trading_number_storage_handle, no_result_counter) -> bool:
    current_price = None
    old_total_profit = None
    # print('trying to locate pLayers price Input ...')
    buy_player_price_input_params = [
        {
            'id': 'delete', 'pic': r'pics\delete_buy_player_price.png', 'to_appear': True,
            'to_disappear': False, 'reg': (1752, 808, 1896 - 1752, 871 - 808), 'con': .9
        },
        {
            'id': 'input', 'pic': r'pics\buy_player_input_field.png', 'to_appear': True,
            'to_disappear': False, 'reg': (1372, 867, 1444 - 1372, 919 - 867), 'con': .85
        }
    ]
    buy_player_price_input_multi = wait_for_multiple(buy_player_price_input_params, max_iterations=5, sleep_dur=1)
    if buy_player_price_input_multi.group():
        if buy_player_price_input_multi.hasattr('location'):
            id, location = buy_player_price_input_multi.group()
            # print('clicking on delete player price') if id == 'delete' else print('clicking into input field')
            pyautogui.click(location)
            rtime(1)

            if id == 'delete':
                # print('cleared previous Players Name ...')
                clear_player_name_input = wait_for(
                    r'pics\buy_player_input_field.png', reg=(1324, 832, 1455 - 1324, 932 - 832),
                    max_iterations=50, sleep_dur=.1, con=.85
                )
                # print(f'{clear_player_name_input = }')
                if clear_player_name_input:
                    # print('entering gathered Player Price ...')
                    pyautogui.click(clear_player_name_input)
                    rtime(1)
        rtype(player.market_price)
        # trading_number_storage_handle.add_sell_price(player.market_price)
        rtime()
        pyautogui.press('enter')
        rtime(1)
    found_at_least_one_arrow = False
    for trying_evaluate_price in range(100):
        """findet in transfermarkt suche statt"""
        if trying_evaluate_price != 0:
            go_back_to_transfer_market_menu()  # go back
            if found_at_least_one_arrow:
                sk_price_minus_btn = locate(r'pics\sk_min_price_minus.png', reg=(1324, 832, 1455 - 1324, 932 - 832))
                if sk_price_minus_btn:
                    pyautogui.click(sk_price_minus_btn)
                    rtime(1)
            else:
                sk_price_plus_btn = locate(r'pics\sk_min_price_plus.png', reg=(1775, 839, 1888 - 1775, 926 - 839))
                if sk_price_plus_btn:
                    pyautogui.doubleClick(sk_price_plus_btn)
                    rtime(1)

        search_button = locate(r'pics\search_button.png', reg=(1313, 1271, 1937 - 1313, 1352 - 1271), con=.75)
        if search_button:
            # print('searching Player...')
            pyautogui.click(search_button)
            rtime(1)
        """findet in suchererebnisse statt"""
        arrows = count_white_arrows()
        if not found_at_least_one_arrow:
            if arrows:
                found_at_least_one_arrow = True
        else:
            if arrows == 0:
                orange_arrow = locate(r'pics\orange_arrow.png', reg=(1499, 284, 1645 - 1499, 389 - 284), con=.75)
                if not orange_arrow:
                    no_player_results_found = locate(
                        r'pics\no_player_results_found.png', reg=(1031, 573, 1674 - 1031, 1025 - 573), con=.75
                    )
                    if no_player_results_found:
                        # print('should go back to trading menu ...')
                        go_back_to_transfer_market_menu()  # go back
                        rtime(1)
                        buy_player_input_field = locate(
                            r'pics\sell_player_input_checkpoint.png', reg=(1699, 862, 1868 - 1699, 919 - 862),
                            con=.8
                        )
                        # plus_market_price = locate(
                        #     r'pics\sk_min_price_plus', reg=(1799, 844, 1874 - 1799, 921 - 844), con=.85
                        # )
                        # pyautogui.click(plus_market_price)
                        # rtime()
                        pyautogui.click(buy_player_input_field)
                        rtime(1)
                        # print('copying evaluated price ...')
                        pyautogui.hotkey('ctrl', 'c')
                        rtime()
                        current_price = clipboard.paste()
                        # trading_number_storage_handle.add_sell_price(int(current_price))
                        print(rf'lowest market value right now is {current_price}')
                        purchase_successful = sniping_player(player, trading_number_storage_handle, current_price, no_result_counter)
                        delete_sniping_filter = wait_for(
                            r'pics\delete_buy_player_price.png', reg=(1770, 688, 1885 - 1770, 740 - 688), sleep_dur=.1,
                            con=.98)
                        if delete_sniping_filter:
                            pyautogui.click(delete_sniping_filter)
                            rtime(1)
                        return purchase_successful


def sniping_player(player, trading_number_storage_handle, current_price, no_result_counter):
    successful_trades = 0
    no_result_counter = 0
    if current_price:
        for trying_buy_optim_player in range(50):
            cycle_filters(player, trying_buy_optim_player)
            search_button = locate(r'pics\search_button.png', reg=(1313, 1271, 1937 - 1313, 1352 - 1271), con=.75)
            if search_button:
                # print('searching for optimal player to buy ...')
                pyautogui.click(search_button)
                rtime(.25)

                """findet in suchererebnisse statt"""


                sniping_player_params = [
                    {
                        'id': 'no_results', 'pic': r'pics\no_player_results_found.png', 'to_appear': True,
                        'to_disappear': False, 'reg': (1031, 573, 1674 - 1031, 1025 - 573), 'con': .9
                    },
                    {
                        'id': 'orange_arrow', 'pic': r'pics\orange_arrow.png', 'to_appear': True,
                        'to_disappear': False, 'reg': (1499, 284, 1645 - 1499, 389 - 284), 'con': .9
                    }
                ]
                sniping_player_params_multi = wait_for_multiple(sniping_player_params, max_iterations=5,
                                                                 sleep_dur=1)
                if sniping_player_params_multi.group():
                    if sniping_player_params_multi.hasattr('location'):
                        id, location = sniping_player_params_multi.group()
                        if id == 'orange_arrow':
                            # print('cleared previous Players Name ...')
                            purchase_player_png = wait_for(
                                r'pics\purchase_player.png', reg=(1570, 762, 1944 - 1570, 848 - 762),
                                con=.75, sleep_dur=.25, max_iterations=15
                            )
                            if purchase_player_png:
                                pyautogui.click(purchase_player_png)
                                rtime(1)
                                purchase_sucessful = purchase_player(current_price, trading_number_storage_handle, no_result_counter)
                                if purchase_sucessful:
                                    # successful_trades = (successful_trades) + 1
                                    # print(f'bought {successful_trades} players and made {}')
                                    return purchase_sucessful
                        if id == 'no_results':
                            go_back_to_transfer_market_menu()
                            no_result_counter += 1
                            if no_result_counter == 35:
                                DBHandler().add_player(player.name)
                        return no_result_counter


def cycle_filters(player, changing_filter):
    """cycle filters for most precise player search"""  # regionen sind richtig
    boolean = False
    if changing_filter % 8 in (0, 4):
        # print('changing min bid price ...')  # changing min bid price
        minus = locate(r'pics\sk_min_price_minus.png', reg=(783, 732, 867 - 783, 810 - 732))
        if not minus:
            plus = locate(r'pics\sk_min_price_plus.png', reg=(1255, 728, 1340 - 1255, 814 - 728))
            if plus:
                pyautogui.click(plus)
        else:
            pyautogui.click(minus)
        rtime(.5)

    elif changing_filter % 8 in (1, 5):
        # print('changing min buy price ...')  # changing min buy price
        minus = locate(r'pics\sk_min_price_minus.png', reg=(790, 843, 861 - 790, 926 - 843))
        if not minus:
            plus = locate(r'pics\sk_min_price_plus.png', reg=(1256, 839, 1339 - 1256, 928 - 839))
            if plus:
                pyautogui.click(plus)
        else:
            pyautogui.click(minus)
        rtime(.5)

    elif changing_filter % 8 == 2:
        # print('selecting quality ...')
        qualitypic_unselected = locate(
            r'pics\qualitypic_unselected.png', reg=(1231, 433, 1346 - 1231, 510 - 433), con=.8
        )
        if qualitypic_unselected:
            pyautogui.click(qualitypic_unselected)
            rtime(.75)
            player_quality_params = {
                'bronze': {
                    'pic': r'pics\bronze_player_quality.png', 'reg': (792, 495, 945 - 792, 561 - 495), 'con': .9
                },
                'silver': {
                    'pic': r'pics\silver_player_quality.png', 'reg': (786, 542, 941 - 786, 607 - 542), 'con': .9
                },
                'gold': {
                    'pic': r'pics\gold_player_quality.png', 'reg': (780, 591, 961 - 780, 658 - 591), 'con': .9
                },
                'special': {
                    'pic': r'pics\special_player_quality.png', 'reg': (773, 640, 945 - 773, 704 - 640), 'con': .9
                }
            }
            qual_to_click = locate(**player_quality_params[player.quality])
            if qual_to_click:
                # print(f'selecting player qualitiy : {player.quality} ...')
                pyautogui.click(qual_to_click)
                rtime(1)

    elif changing_filter % 8 == 3:
        # print('selecting rarity ...')
        raritypic_unselected = locate(
            r'pics\qualitypic_unselected.png', reg=(1783, 424, 1874 - 1783, 495 - 424), con=.8
        )  # r'pics\qualitypic_unscelect = r'pics\raritypic_unselect
        if raritypic_unselected:
            pyautogui.click(raritypic_unselected)
            rtime(.75)
            player_rarity_params = {
                'non-rare': {
                    'pic': r'pics\common_player_rarity.png', 'reg': (1327, 498, 1494 - 1327, 558 - 498), 'con': .9
                },
                'rare': {
                    'pic': r'pics\rare_player_rarity.png', 'reg': (1328, 544, 1483 - 1328, 608 - 544), 'con': .9
                },
                'totw': {
                    'pic': r'pics\totw_player_rarity.png', 'reg': (1330, 600, 1558 - 1330, 646 - 600), 'con': .9
                }
            }
            rari_to_click = locate(**player_rarity_params[player.rarity])
            if rari_to_click:
                # print(f'selecting player rarity : {player.rarity} ...')
                pyautogui.click(rari_to_click)
                rtime(1)

    elif changing_filter % 8 == 6:
        deselect_player_rarity = locate(
            r'pics\deselect_player_rarity.png', reg=(1750, 417, 1900 - 1750, 500 - 417)
        )
        if deselect_player_rarity:
            pyautogui.click(deselect_player_rarity)
            rtime(.75)
    elif changing_filter == 7:
        deselect_player_quality = locate(
            r'pics\deselect_player_rarity.png', reg=(1259, 440, 1322 - 1259, 501 - 440), con=.8
        )
        if deselect_player_quality:
            pyautogui.click(deselect_player_quality)
            rtime(.75)


def purchase_player(current_price, trading_number_storage_handle, no_result_counter):
    purchase_sucessful = False
    confirm_purchase = wait_for(
        r'pics\confirm_purchase_player.png', reg=(1195, 755, 1375 - 1195, 847 - 755), sleep_dur=.25, max_iterations=15
    )
    if purchase_player:
        print('trying to buy Player ...')
        pyautogui.press('Enter')
        rtime(1)
        # pyautogui.press('Enter')
        # rtime()
        print(
            'checking if purchase was successful ...')  ################################## needs to be checked later !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
        # successful_purchase = wait_for(
        #     r'pics\purchase_was_successful.png', reg=(717, 261, 842 - 717, 311 - 261), sleep_dur=.25, con=0.5
        # )
        successful_purchase = pyautogui.pixelMatchesColor(746, 293, (54, 184, 75), tolerance=42)
        if successful_purchase:
            no_result_counter = 0
            transfer_market_sell_btn = locate(
                r'pics\transfer_market_sell_btn.png', reg=(1560, 641, 1794 - 1560, 710 - 641))
            pyautogui.click(transfer_market_sell_btn)
            rtime(1)
            sell_player_input_checkpoint = locate(
                r'pics\sell_player_input_checkpoint.png', reg=(1818, 770, 1896 - 1818, 817 - 770))
            pyautogui.click(sell_player_input_checkpoint)
            rtime(1)
            int_current_prize = int(current_price)
            sell_price = int(int_current_prize * 1.15)
            sell_price = round(sell_price, -2)
            min_trade_profit = int(sell_price * 0.95) - int_current_prize
            trading_number_storage_handle.add_min_profit(min_trade_profit)
            # trading_number_storage_handle.add_sell_price(sell_price)
            print(trading_number_storage_handle.to_dict())
            # print(f'selling for = {sell_price} coins !')
            # print(f'made min. {sell_price_difference} coins profit !')
            # print(f'made min. {int(total_min_profit)} total coins profit !')
            str_sell_price = str(sell_price)
            rtype(str_sell_price)
            rtime(1)
            sell_player_input_checkpoint = locate(
                r'pics\sell_player_input_checkpoint.png', reg=(1826, 847, 1898 - 1826, 891 - 847))
            pyautogui.click(sell_player_input_checkpoint)
            rtime(1)
            rtype(str_sell_price)
            rtime(1)
            confirm_sell_player = locate(
                r'pics\confirm_sell_player.png', reg=(1681, 971, 1819 - 1681, 1037 - 971), con=.85)
            pyautogui.click(confirm_sell_player)
            rtime(1.5)
        go_back_to_transfer_market_menu()
    return purchase_sucessful


def go_back_to_transfer_market_menu():
    search_results = wait_for(
        r'pics\buy_player_checkpoint.png', reg=(124, 91, 465 - 124, 218 - 91), max_iterations=50, sleep_dur=.1
    )
    if search_results:
        # print('going back to Trading Menu ...')
        back_button = wait_for(r'pics\back_button.png', reg=(81, 104, 203 - 81, 208 - 104), max_iterations=50,
                               sleep_dur=.1, con=.7)
        rtime()
        pyautogui.click(back_button)
        rtime(1)


def count_white_arrows():
    buy_player_checkpoint = wait_for(
        r'pics\buy_player_checkpoint.png', reg=(157, 119, 436 - 157, 193 - 119), max_iterations=80, sleep_dur=.1
    )
    if buy_player_checkpoint:
        # print('Found buy_player_checkpoint !')
        white_arrows = locate_consecutively(r'pics\white_arrow.png', .9, (1502, 411, 1613 - 1502, 1268 - 411))
        length = len(white_arrows)
        # print(rf'found {length} x same players')
        return length


def clear_transfer_list():
    # locate sold items
    sold_items = locate(r'pics\delete_sold_players.png', reg=(1413, 277, 1580 - 1413, 339 - 277))
    if sold_items:
        # click sold items
        pyautogui.click(sold_items)
        rtime(1.5)
    # locate not sold items
    reselling_player = locate(r'pics\reselling_players.png', reg=(1414, 485, 1574 - 1414, 552 - 485))
    if reselling_player:
        # click not sold items
        pyautogui.click(reselling_player)
        rtime(1)
        # confirm reselling for same price -> min_profit
        confirm_reselling_player = wait_for(r'pics\confirm_reselling_players.png',
                                            reg=(1219, 823, 1339 - 1219, 875 - 823))
        if confirm_reselling_player:
            pyautogui.click(confirm_reselling_player)
            rtime(1)
    pass


def screenshot_initial_bank_account():
    import os
    initial_bank_account = pyautogui.screenshot('initial_bank_account.png', region=(2068, 118, 2334 - 2068, 149 - 118))
    initial_bank_account.save(r'..\pics\initial_bank_account.png')
    rtime()
    os.system(r"initial_bank_account.png")


def screenshot_transfer_list_details():
    import os
    transfer_list_details = pyautogui.screenshot('transfer_list_details.png', region=(890, 643, 1115 - 890, 726 - 643))
    transfer_list_details.save(r'..\pics\transfer_list_details.png')
    rtime()
    os.system(r"transfer_list_details.png")


def failsafe():
    pass  # login


if __name__ == '__main__':
    screenshot_initial_bank_account()
    pass
