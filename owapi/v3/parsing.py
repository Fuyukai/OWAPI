"""
Parsing the data returned from Blizzard.
"""
from lxml import etree

from owapi import util
from owapi.prestige import PRESTIGE_BORDERS, PRESTIGE_STARS

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
    "sombra": "0x02E000000000012E",
    "orisa": "0x02E000000000013E",
    "doomfist": "0x02E000000000012F",
    "moira": "0x02E00000000001A2",
    "brigitte": "0x02E0000000000195",
    "wrecking_ball": "0x02E00000000001CA",
    "ashe": "0x02E0000000000200",
    "baptiste": "0x02E0000000000221",
    "sigma": "0x02E000000000023B",
    "echo": "0x02E0000000000206",
}

tier_data_img_src = {
    "rank-BronzeTier.png": "bronze",
    "rank-SilverTier.png": "silver",
    "rank-GoldTier.png": "gold",
    "rank-PlatinumTier.png": "platinum",
    "rank-DiamondTier.png": "diamond",
    "rank-MasterTier.png": "master",
    "rank-GrandmasterTier.png": "grandmaster",
}

role_data_img_src = {
    "icon-tank-8a52daaf01.png": "tank",
    "icon-offense-6267addd52.png": "damage",
    "icon-support-46311a4210.png": "support",
}


def bl_parse_stats(parsed, mode="quickplay", status=None):
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
    if not status or status.lower() != "public profile":
        hasrank = parsed.xpath('//*[@id="overview-section"]/div/div/div/div/div[2]/div/div[3]/div')
        if hasrank:
            comprank = int(hasrank[0].text)
        else:
            comprank = None
        built_dict["overall_stats"]["comprank"] = comprank
        return built_dict

    mast_head = parsed.xpath(".//div[@class='masthead-player']")[0]

    # Rank images are now based on 2 separate images. Prestige now also relies on 'player-rank' element
    prestige_stars = 0
    try:
        prestige_rank = mast_head.xpath(".//div[@class='player-rank']")[0]
        bg_image = [x for x in prestige_rank.values() if "background-image" in x][0]
    except IndexError:
        # No stars
        prestige_stars = 0
    else:
        for key, val in PRESTIGE_STARS.items():
            if key in bg_image:
                prestige_stars = val
                # Adds a new dict key called "prestige_image". Left the old name below of "rank_image" for compatibility
                built_dict["overall_stats"]["prestige_image"] = bg_image.split("(")[1][:-1]
                break
            else:
                # Unknown prestige image
                prestige_stars = None

    # Extract the background-image from the styles.
    prestige_num = 0
    try:
        # Get the player-level base (border).
        prestige = mast_head.xpath(".//div[@class='player-level']")[0]
        bg_image = [x for x in prestige.values() if "background-image" in x][0]
    except IndexError:
        # Cannot find background-image.
        # Yikes!
        # Don't set a prestige.
        built_dict["overall_stats"]["prestige"] = 0
    else:
        for key, val in PRESTIGE_BORDERS.items():
            if key in bg_image:
                prestige_num = val
                built_dict["overall_stats"]["rank_image"] = bg_image.split("(")[1][:-1]
                break
        else:
            # Unknown rank image
            prestige_num = None

    # If we have prestige values, return them. Otherwise, return None
    if prestige_num is not None and prestige_stars is not None:
        built_dict["overall_stats"]["prestige"] = prestige_num + prestige_stars
    else:
        built_dict["overall_stats"]["prestige"] = None

    # Parse out the HTML.
    level = int(prestige.findall(".//div")[0].text)
    built_dict["overall_stats"]["level"] = level

    # Get and parse out endorsement level.
    endorsement_level = int(
        mast_head.xpath(".//div[@class='EndorsementIcon-tooltip']/div[@class='u-center']")[0].text
    )
    built_dict["overall_stats"]["endorsement_level"] = endorsement_level

    # Get endorsement circle.
    endorsement_icon_inner = mast_head.xpath(
        ".//div[@class='endorsement-level']/div[@class='EndorsementIcon']/div["
        "@class='EndorsementIcon-inner']"
    )[0]

    # Get individual endorsement segments.
    names = ("shotcaller", "teammate", "sportsmanship")
    for name in names:
        try:
            endorsement_value = endorsement_icon_inner.findall(
                f".//svg[@class='EndorsementIcon-border EndorsementIcon-border--{name}']"
            )[0].get("data-value")
        except:  # TODO: don't do this...
            endorsement_value = 0

        val = float(endorsement_value)
        built_dict["overall_stats"][f"endorsement_{name}"] = val

    # Get comp rank.
    try:
        for role in mast_head.xpath(".//div[@class='competitive-rank']")[0]:
            role_img = role.findall(".//img[@class='competitive-rank-role-icon']")[0]
            role_img_src = role_img.values()[1]
            role_str = ""
            for key, val in role_data_img_src.items():
                if key in role_img_src:
                    role_str = val
                    break
            built_dict["overall_stats"][role_str + "_role_image"] = role_img_src

            tier_img = role.findall(".//img[@class='competitive-rank-tier-icon']")[0]
            tier_img_src = tier_img.values()[1]
            tier_str = ""
            for key, val in tier_data_img_src.items():
                if key in tier_img_src:
                    tier_str = val
                    break
            built_dict["overall_stats"][role_str + "_tier_image"] = tier_img_src

            built_dict["overall_stats"][role_str + "_tier"] = tier_str

            hasrank = role.findall(".//div[@class='competitive-rank-level']")
            if hasrank:
                comprank = int(hasrank[0].text)
            else:
                comprank = None
            built_dict["overall_stats"][role_str + "_comprank"] = comprank

    except IndexError as exc:
        print(str(exc))
    finally:
        for role in ["tank", "damage", "support"]:
            if role + "_role_image" not in built_dict["overall_stats"]:
                built_dict["overall_stats"][role + "_role_image"] = None
            if role + "_tier_image" not in built_dict["overall_stats"]:
                built_dict["overall_stats"][role + "_tier_image"] = None
            if role + "_tier" not in built_dict["overall_stats"]:
                built_dict["overall_stats"][role + "_tier"] = None
            if role + "_comprank" not in built_dict["overall_stats"]:
                built_dict["overall_stats"][role + "_comprank"] = None

    # Fetch Avatar
    avatar_root = mast_head.find(".//img[@class='player-portrait']")
    # some profiles don't have an avatar url?
    # it's just a <img class="player-portrait"> ???
    if avatar_root is not None:
        try:
            avatar_url = avatar_root.attrib["src"]
        except KeyError:
            avatar_url = None
    else:
        avatar_url = None

    built_dict["overall_stats"]["avatar"] = avatar_url

    if mode == "competitive":
        # the competitive overview is under a div with id='competitive'
        # and the right category
        try:
            stat_groups = parsed.xpath(
                ".//div[@id='competitive']"
                "//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']"
            )[0]
        except IndexError:
            # No stats
            return None
    elif mode == "quickplay":
        try:
            stat_groups = parsed.xpath(
                ".//div[@id='quickplay']"
                "//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']"
            )[0]
        except IndexError:
            # User has no stats...
            return None
    else:
        # how else to handle fallthrough case?
        stat_groups = parsed.xpath(
            ".//div[@data-group-id='stats' and @data-category-id='0x02E00000FFFFFFFF']"
        )[0]

    # Highlight specific stat groups.
    try:
        game_box = stat_groups[3]
    except IndexError:
        try:
            game_box = stat_groups[2]  # I guess use 2?
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
            losses = int(
                game_box.xpath(".//text()[. = 'Games Lost']/../..")[0][1].text.replace(",", "")
            )
            ties = int(
                game_box.xpath(".//text()[. = 'Games Tied']/../..")[0][1].text.replace(",", "")
            )
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
            wr = round((wins / (games - ties)) * 100, 2)

        built_dict["overall_stats"]["ties"] = ties
        built_dict["overall_stats"]["games"] = games
        built_dict["overall_stats"]["losses"] = losses
        built_dict["overall_stats"]["win_rate"] = wr

    # Update the dictionary.
    built_dict["overall_stats"]["wins"] = wins

    # Build a dict using the stats.
    game_stats = {}
    average_stats = {}
    rolling_average_stats = {}

    for subbox in stat_groups:
        trs = subbox.findall(".//tbody/tr")
        # Update the dict with [0]: [1]
        for subval in trs:
            name, value = util.sanitize_string(subval[0].text), subval[1].text
            # Try and parse out the value. It might be a time!
            # If so, try and extract the time.
            nvl = util.try_extract(value)

            if "average" in name.lower():
                name = name.replace("_average", "_avg")
                into = average_stats
            elif "_avg_per_10_min" in name.lower():
                # 2017-08-03 - calculate rolling averages.
                name = name.lower().replace("_avg_per_10_min", "")
                into = rolling_average_stats
            else:
                into = game_stats

            # Correct Blizzard Singular Plural Bug
            if "_plural_" in name:
                name = util.correct_plural_name(name, nvl)

            into[name] = nvl

    # Manually add the KPD.
    try:
        game_stats["kpd"] = round(game_stats["eliminations"] / game_stats["deaths"], 2)
    except KeyError:
        # They don't have any eliminations/deaths.
        # Set the KPD to 0.0.
        # See: #106
        game_stats["kpd"] = 0

    built_dict["game_stats"] = game_stats
    built_dict["average_stats"] = average_stats
    built_dict["rolling_average_stats"] = rolling_average_stats
    built_dict["competitive"] = mode == "competitive"

    if "games" not in built_dict["overall_stats"]:
        # manually calculate it
        # 2017-07-04 - changed to use eliminations
        # since damage done gave a bit of a stupid amount
        # 2017-07-11 - changed to cycle some averages
        average_keys = ("eliminations", "healing_done", "final_blows", "objective_kills")
        for key in average_keys:
            try:
                total = built_dict["game_stats"][key]
                avg = built_dict["average_stats"][key + "_avg"]
            except KeyError:
                continue
            else:
                got = True
                break
        else:
            got = False

        if got:
            games = int(total // avg)

            losses = games - built_dict["overall_stats"]["wins"]
            built_dict["overall_stats"]["games"] = games
            built_dict["overall_stats"]["losses"] = losses
            built_dict["overall_stats"]["win_rate"] = round(
                (built_dict["overall_stats"]["wins"] / games) * 100, 2
            )
        else:
            # lol make them up
            built_dict["overall_stats"]["games"] = 0
            built_dict["overall_stats"]["losses"] = 0
            built_dict["overall_stats"]["win_rate"] = 0

    return built_dict


def bl_parse_all_heroes(parsed, mode="quickplay"):
    built_dict = {}

    _root = parsed.xpath(".//div[@id='{}']".format(mode))

    # maybe this isn't needed anymore??
    try:
        # XPath for the `u-align-center` h6 which signifies there's no data.
        no_data = _root[0].xpath(".//ul/h6[@class='u-align-center']")[0]
    except IndexError:
        pass
    else:
        if no_data.text.strip() == "We don't have any data for this account in this mode yet.":
            return None

    if mode == "competitive":
        # Fix for #287. The competitive play section doesn't exist if the user doesn't have any
        # competitive playtime.
        try:
            _root = parsed.findall(".//div[@data-mode='competitive']")[0]
        except IndexError:
            return None
    else:
        _root = parsed

    _hero_info = _root.xpath(
        ".//div[@data-group-id='comparisons' and " "@data-category-id='0x0860000000000021']"
    )[0]
    hero_info = _hero_info.findall(".//div[@class='ProgressBar-textWrapper']")

    # Loop over each one, extracting the name and hours counted.
    percent_per_second = None
    for child in reversed(hero_info):
        name, played = child.getchildren()
        if not name.text:
            continue

        name, played = util.sanitize_string(name.text), played.text.lower()

        time = 0
        if played != "--":
            time = util.try_extract(played)

        # More accurate playtime calculation
        # Requires reversing hero_info
        category_item = child.getparent().getparent()
        percent = float(category_item.attrib["data-overwatch-progress-percent"])
        if percent_per_second is None and 1 > time > 0:
            seconds = 3600 * time
            percent_per_second = percent / seconds

        built_dict[name] = time
        if percent_per_second is not None:
            built_dict[name] = (percent / percent_per_second) / float(3600)

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
        no_data = _root[0].xpath(".//ul/h6[@class='u-align-center']")[0]
    except IndexError:
        pass
    else:
        if no_data.text.strip() == "We don't have any data for this account in this mode yet.":
            return None

    for hero_name, requested_hero_div_id in hero_data_div_ids.items():
        n_dict = {}
        _stat_groups = _root[0].xpath(
            ".//div[@data-group-id='stats' and @data-category-id='{0}']".format(
                requested_hero_div_id
            )
        )

        if not _stat_groups:
            continue

        stat_groups = _stat_groups[0]
        _average_stats = {}
        _t_d = {}
        _rolling_avgs = {}
        # offset for subboxes
        # if there IS a hero-specific box, we need to scan all boxes from offset to end
        # because the hero-specific box is first.
        # if there is NOT, we scan all boxes later.
        # this is determined by the xpath to find the Hero Specific page.
        subbox_offset = 0

        # .find on the assumption hero box is the *first* item
        hbtitle = None
        try:
            hbtitle = stat_groups.find(".//span[@class='stat-title']").text
        except AttributeError:
            try:
                hbtitle = stat_groups.find(".//h5[@class='stat-title']").text
            except AttributeError:
                # Unable to parse stat boxes. This is likely due to 0 playtime on a hero, so there are no stats
                pass

        for idx, sg in enumerate(stat_groups):
            stat_group_hero_specific = stat_groups[idx].find('.//*[@class="stat-title"]').text

            if stat_group_hero_specific.lower() == "hero specific":
                try:
                    hero_specific_box = stat_groups[idx]
                    trs = hero_specific_box.findall(".//tbody/tr")

                    # Update the dict with [0]: [1]
                    for subval in trs:
                        name, value = util.sanitize_string(subval[0].text), subval[1].text

                        # Put averages into average_stats
                        if "_avg_per_10_min" in name.lower():
                            into = _rolling_avgs
                            name = name.lower().replace("_avg_per_10_min", "")
                        else:
                            into = _t_d
                        nvl = util.try_extract(value)
                        into[name] = nvl
                    break
                except IndexError:
                    pass

        n_dict["hero_stats"] = _t_d
        _t_d = {}

        for subbox in stat_groups[subbox_offset:]:
            trs = subbox.findall(".//tbody/tr")
            # Update the dict with [0]: [1]
            for subval in trs:
                name, value = util.sanitize_string(subval[0].text), subval[1].text

                if "_avg_per_10_min" in name:
                    into = _rolling_avgs
                    name = name.replace("_avg_per_10_min", "")
                elif name in n_dict["hero_stats"]:
                    into = None
                else:
                    into = _t_d

                nvl = util.try_extract(value)

                # Correct Blizzard Singular Plural Bug
                if "_plural_" in name:
                    name = util.correct_plural_name(name, nvl)

                if into != None:
                    into[name] = nvl

        n_dict["general_stats"] = _t_d
        n_dict["average_stats"] = _average_stats
        n_dict["rolling_average_stats"] = _rolling_avgs

        built_dict[hero_name] = n_dict

    return built_dict


def bl_parse_achievement_data(parsed: etree._Element, mode="quickplay"):
    # Start the dict.
    built_dict = {}

    _root = parsed.xpath(".//section[@id='achievements-section']")
    if not _root:
        return
    _root = _root[0]

    _category_selects = _root.xpath(".//select[@data-group-id='achievements']")[0].xpath(
        ".//option"
    )

    for _category_select in _category_selects:
        category_name = _category_select.text
        category_id = _category_select.get("value")

        _achievement_boxes = _root.xpath(
            ".//div[@data-group-id='achievements' and @data-category-id='{0}']"
            "/ul/div/div[@data-tooltip]".format(category_id)
        )
        n_dict = {}

        for _achievement_box in _achievement_boxes:
            achievement_name = _achievement_box.xpath("./div/div")[0].text
            if achievement_name == "?":
                # Sombra ARG clue, not a real achievement
                continue

            n_dict[
                util.sanitize_string(achievement_name)
            ] = "m-disabled" not in _achievement_box.get("class")

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
