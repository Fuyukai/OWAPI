"""
Parsing the data returned from Blizzard.
"""
from lxml import etree
from math import floor

import unidecode
import re

from owapi import util
from owapi.prestige import PRESTIGE

hero_data_div_ids = {
    "reaper": "0x02E0000000000002",
    "tracer": "0x02E0000000000003",
    "mercy": "0x02E0000000000004",
    "hanzo": "0x02E0000000000005",
    "torbjorn": "0x02E0000000000006",
    "reinhardt": "0x02E0000000000007",
    "pharah": "0x02E0000000000008",
    "winston": "0x02E0000000000009",
    "widowmaker": "0x02E000000000000A",
    "bastion": "0x02E0000000000015",
    "symmetra": "0x02E0000000000016",
    "zenyatta": "0x02E0000000000020",
    "genji": "0x02E0000000000029",
    "roadhog": "0x02E0000000000040",
    "mccree": "0x02E0000000000042",
    "junkrat": "0x02E0000000000065",
    "zarya": "0x02E0000000000068",
    "soldier76": "0x02E000000000006E",
    "lucio": "0x02E0000000000079",
    "dva": "0x02E000000000007A",
    "mei": "0x02E00000000000DD",
    "ana": "0x02E000000000013B",
    "sombra": "0x02E000000000012E"
}

tier_data_img_src = {
    "rank-1.png": "bronze",
    "rank-2.png": "silver",
    "rank-3.png": "gold",
    "rank-4.png": "platinum",
    "rank-5.png": "diamond",
    "rank-6.png": "master",
    "rank-7.png": "grandmaster"
}


def bl_parse_stats(parsed, mode="quickplay"):
    # Just a quick FYI
    # If future me or future anyone else is looking at this, I do not how this code works.
    # I'm really really hoping it doesn't break.
    # Good luck!

    try:
        # XPath for the `u-align-center` h6 which signifies there's no data.
        no_data = parsed.xpath(".//div[@id='{}']//ul/h6[@class='u-align-center']".format(mode))[0]
    except IndexError:
        pass
    else:
        if no_data.text.strip() == "We don't have any data for this account in this mode yet.":
            return None

    # Start the dict.
    built_dict = {"game_stats": [], "overall_stats": {}, "average_stats": []}

    # Shortcut location for player level etc
    mast_head = parsed.xpath(".//div[@class='masthead-player']")[0]

    # Get the prestige.
    prestige = mast_head.xpath(".//div[@class='player-level']")[0]
    # Extract the background-image from the styles.
    try:
        bg_image = [x for x in prestige.values() if 'background-image' in x][0]
    except IndexError:
        # Cannot find background-image.
        # Yikes!
        # Don't set a prestige.
        built_dict["overall_stats"]["prestige"] = 0
    else:
        for key, val in PRESTIGE.items():
            if key in bg_image:
                prestige_num = val
                built_dict["overall_stats"]["rank_image"] = bg_image.split("(")[1][:-1]
                break
        else:
            # Unknown.
            prestige_num = None
        built_dict["overall_stats"]["prestige"] = prestige_num

    # Parse out the HTML.
    level = int(prestige.findall(".//div")[0].text)
    built_dict["overall_stats"]["level"] = level

    try:
        tier = mast_head.xpath(".//div[@class='competitive-rank']/img")[0]
        img_src = [x for x in tier.values() if 'rank-icons' in x][0]
    except IndexError:
        built_dict['overall_stats']['tier'] = None
    else:
        for key, val in tier_data_img_src.items():
            if key in img_src:
                tier_str = val
                break
        else:
            tier_str = None
        built_dict["overall_stats"]["tier"] = tier_str

    hasrank = mast_head.findall(".//div[@class='competitive-rank']/div")
    if hasrank:
        comprank = int(hasrank[0].text)
    else:
        comprank = None
    built_dict["overall_stats"]["comprank"] = comprank

    # Fetch Avatar
    built_dict["overall_stats"]["avatar"] = mast_head.find(".//img[@class='player-portrait']").attrib['src']

    if mode == "competitive":
        hascompstats = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")
        if len(hascompstats) != 2:
            return None
        stat_groups = hascompstats[1]
    elif mode == "quickplay":
        try:
            stat_groups = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")[0]
        except IndexError:
            # User has no stats...
            return None
    else:
        # how else to handle fallthrough case?
        stat_groups = parsed.xpath(".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']")[0]

    # Highlight specific stat groups.
    try:
        game_box = stat_groups[6]
    except IndexError:
        try:
            game_box = stat_groups[5]
        except IndexError:
            # edge cases...
            # we can't really extract any more stats
            # so we do an early return
            return {}

    # Calculate the wins, losses, and win rate.
    try:
        wins = int(game_box.xpath(".//text()[. = 'Games Won']/../..")[0][1].text.replace(",", ""))
    except IndexError:
        # weird edge case
        wins = 0
    g = game_box.xpath(".//text()[. = 'Games Played']/../..")
    if len(g) < 1:
        # Blizzard fucked up, temporary quick fix for #70
        games, losses = None, None
    else:
        games = int(g[0][1].text.replace(",", ""))

    if mode == "competitive":
        try:
            misc_box = stat_groups[7]
            losses = int(misc_box.xpath(".//text()[. = 'Games Lost']/../..")[0][1].text.replace(",", ""))
            ties = int(misc_box.xpath(".//text()[. = 'Games Tied']/../..")[0][1].text.replace(",", ""))
        except IndexError:
            # Sometimes the losses and ties don't exist.
            # I'm not 100% as to what causes this, but it might be because there are no ties.
            # In this case, just set ties to 0, and calculate losses manually.
            ties = 0
            # Quickplay shit.
            # Goddamnit blizzard.
            if games is None:
                losses = 0
                games = 0
                wins = 0
            else:
                # Competitive stats do have these values (for now...)
                losses = games - wins

        if games == 0 or games == ties:
            wr = 0
        else:
            wr = floor((wins / (games - ties)) * 100)

        built_dict["overall_stats"]["ties"] = ties
        built_dict["overall_stats"]["games"] = games
        built_dict["overall_stats"]["losses"] = losses
        built_dict["overall_stats"]["win_rate"] = wr

    # Update the dictionary.
    built_dict["overall_stats"]["wins"] = wins

    # Build a dict using the stats.
    _t_d = {}
    _a_d = {}
    for subbox in stat_groups:
        trs = subbox.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = util.sanitize_string(subval[0].text), subval[1].text
            # Try and parse out the value. It might be a time!
            # If so, try and extract the time.
            nvl = util.try_extract(value)
            if 'average' in name.lower():
                _a_d[name.replace("_average", "_avg")] = nvl
            else:
                _t_d[name] = nvl

    # Manually add the KPD.
    try:
        _t_d["kpd"] = round(_t_d["eliminations"] / _t_d["deaths"], 2)
    except KeyError:
        # They don't have any eliminations/deaths.
        # Set the KPD to 0.0.
        # See: #106
        _t_d["kpd"] = 0

    built_dict["game_stats"] = _t_d
    built_dict["average_stats"] = _a_d
    built_dict["competitive"] = mode == "competitive"

    return built_dict


def bl_parse_all_heroes(parsed, mode="quickplay"):
    built_dict = {}

    _root = parsed.xpath(".//div[@id='{}']".format(mode))
    try:
        # XPath for the `u-align-center` h6 which signifies there's no data.
        no_data = _root[0].xpath(".//ul/h6[@class='u-align-center']".format(mode))[0]
    except IndexError:
        pass
    else:
        if no_data.text.strip() == "We don't have any data for this account in this mode yet.":
            return None

    if mode == "competitive":
        _root = parsed.findall(".//div[@data-mode='competitive']")[0]
    else:
        _root = parsed

    _hero_info = _root.findall(".//div[@data-group-id='comparisons']")[0]
    hero_info = _hero_info.findall(".//div[@class='bar-text']")

    # Loop over each one, extracting the name and hours counted.
    for child in hero_info:
        name, played = child.getchildren()
        name, played = util.sanitize_string(name.text), played.text.lower()

        if played == "--":
            time = 0
        else:
            time = util.try_extract(played)
        built_dict[name] = time

    return built_dict


def bl_parse_hero_data(parsed: etree._Element, mode="quickplay"):
    # Start the dict.
    built_dict = {}

    _root = parsed.xpath(
        ".//div[@id='{}']".format("competitive" if mode == "competitive" else "quickplay")
    )
    if not _root:
        return None

    try:
        # XPath for the `u-align-center` h6 which signifies there's no data.
        no_data = _root[0].xpath(".//ul/h6[@class='u-align-center']".format(mode))[0]
    except IndexError:
        pass
    else:
        if no_data.text.strip() == "We don't have any data for this account in this mode yet.":
            return None

    for hero_name, requested_hero_div_id in hero_data_div_ids.items():
        n_dict = {}
        _stat_groups = _root[0].xpath(
            ".//div[@data-group-id='stats' and @data-category-id='{0}']".format(requested_hero_div_id)
        )

        if not _stat_groups:
            continue

        stat_groups = _stat_groups[0]
        _average_stats = {}

        _t_d = {}
        hero_specific_box = stat_groups[0]
        trs = hero_specific_box.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = util.sanitize_string(subval[0].text), subval[1].text

            # Put averages into average_stats
            if "average" in name:
                into = _average_stats
            else:
                into = _t_d
            nvl = util.try_extract(value)
            into[name] = nvl

        n_dict["hero_stats"] = _t_d

        _t_d = {}
        for subbox in stat_groups[1:]:
            trs = subbox.findall(".//tbody/tr")
            # Update the dict with [0]: [1]
            for subval in trs:
                name, value = util.sanitize_string(subval[0].text), subval[1].text
                # Put averages into average_stats
                if "average" in name:
                    into = _average_stats
                else:
                    into = _t_d
                nvl = util.try_extract(value)
                into[name] = nvl

        n_dict["general_stats"] = _t_d
        n_dict["average_stats"] = _average_stats

        built_dict[hero_name] = n_dict

    return built_dict


def bl_parse_achievement_data(parsed: etree._Element, mode="quickplay"):
    # Start the dict.
    built_dict = {}

    _root = parsed.xpath(
        ".//section[@id='achievements-section']"
    )
    if not _root:
        return
    _root = _root[0]

    _category_selects = _root.xpath(".//select[@data-group-id='achievements']")[0].xpath(".//option")

    for _category_select in _category_selects:
        category_name = _category_select.text
        category_id = _category_select.get("value")

        _achievement_boxes = _root.xpath(
            ".//div[@data-group-id='achievements' and @data-category-id='{0}']/ul/div/div[@data-tooltip]".format(
                category_id))
        n_dict = {}

        for _achievement_box in _achievement_boxes:
            achievement_name = _achievement_box.xpath("./div/div")[0].text
            if achievement_name == '?':
                # Sombra ARG clue, not a real achievement
                continue

            n_dict[util.sanitize_string(achievement_name)] = "m-disabled" not in _achievement_box.get("class")

        built_dict[category_name.lower()] = n_dict

    return built_dict


def bl_find_heroes(parsed: etree._Element):
    # Start the dict.
    built_dict = {"role": "", "difficulty": "", "abilities": {}}

    difficulty = len(parsed.findall(".//span[@class='star']"))
    role = parsed.xpath(".//h4[@class='h2 hero-detail-role-name']")[0].text
    _abilities = parsed.findall(".//div[@class='hero-ability-descriptor']")
    abilities = {}

    for ability in _abilities:
        name, description = ability[0].text, ability[1].text
        abilities[name] = description

    built_dict["difficulty"] = difficulty
    built_dict["role"] = role
    built_dict["abilities"] = abilities

    return built_dict


def bl_get_all_heroes(parsed: etree._Element):
    _heroes = parsed.findall(".//a[@class='hero-portrait-detailed']")
    heroes = [hero.get("data-hero-id") for hero in _heroes]
    return heroes
