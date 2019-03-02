export interface OWAPIBlob {
  _request: {
    api_ver: Number
    route: String
  }

  any: null;
  eu: Region?;
  kr: Region?;
  us: Region?;

  msg?: String;
  error?: Number | "Private";
}

interface Region {
  achievements: {
    damage: {
      [x: string]: Boolean
      air_strike: Boolean
      armor_up: Boolean
      charge: Boolean
      clearing_the_area: Boolean
      cold_snap: Boolean
      cratered: Boolean
      death_from_above: Boolean
      did_that_sting: Boolean
      die_die_die_die: Boolean
      hack_the_planet: Boolean
      huge_success: Boolean
      ice_blocked: Boolean
      its_high_noon: Boolean
      mine_like_a_steel_trap: Boolean
      power_outage: Boolean
      raid_wipe: Boolean
      roadkill: Boolean
      rocket_man: Boolean
      served_up: Boolean
      short_fuse: Boolean
      simple_geometry: Boolean
      slice_and_dice: Boolean
      smooth_as_silk: Boolean
      special_delivery: Boolean
      target_rich_environment: Boolean
      the_car_wash: Boolean
      the_dragon_is_sated: Boolean
      their_own_worst_enemy: Boolean
      total_recall: Boolean
      triple_threat: Boolean
      waste_not_want_not: Boolean
      whoa_there: Boolean
    }
    general: {
      [x: string]: Boolean
      blackjack: Boolean
      centenary: Boolean
      decked_out: Boolean
      decorated: Boolean
      level_10: Boolean
      level_25: Boolean
      level_50: Boolean
      survival_expert: Boolean
      the_friend_zone: Boolean
      the_path_is_closed: Boolean
      undying: Boolean
    }
    maps: {
      [x: string]: Boolean
      cant_touch_this: Boolean
      double_cap: Boolean
      escort_duty: Boolean
      lockdown: Boolean
      shutout: Boolean
      world_traveler: Boolean
    }
    special: {
      [x: string]: Boolean
      a_couple_of_flakes: Boolean
      a_quiet_night: Boolean
      ambush: Boolean
      clean_getaway: Boolean
      cleanup_duty: Boolean
      cool_as_ice: Boolean
      dawn_breaks: Boolean
      dawn_patrol: Boolean
      distinguished_service: Boolean
      flagbearer: Boolean
      four_they_were: Boolean
      handle_with_care: Boolean
      hardened_defenders: Boolean
      held_the_door: Boolean
      hot_hand: Boolean
      into_the_shadows: Boolean
      lucio_hat_trick: Boolean
      mission_complete: Boolean
      not_a_scratch: Boolean
      plausible_deniability: Boolean
      rampage: Boolean
      redacted: Boolean
      replacements: Boolean
      safe_hands: Boolean
      six_they_were: Boolean
      six_wanderers: Boolean
      snowed_in: Boolean
      strike_team: Boolean
      survived_the_night: Boolean
      survivor: Boolean
      the_venice_incident: Boolean
      thinking_with_your_stomach: Boolean
      unit_commendation: Boolean
      unscathed: Boolean
      volley: Boolean
      whap: Boolean
      yeti_catcher: Boolean
    }
    support: {
      [x: string]: Boolean
      antipode: Boolean
      enabler: Boolean
      excuse_me: Boolean
      grounded: Boolean
      group_health_plan: Boolean
      huge_rez: Boolean
      naptime: Boolean
      rapid_discord: Boolean
      simple_trigonometry: Boolean
      supersonic: Boolean
      the_floor_is_lava: Boolean
      the_iris_embraces_you: Boolean
    }
    tank: {
      [x: string]: Boolean
      adaptation: Boolean
      anger_management: Boolean
      game_over: Boolean
      giving_you_the_hook: Boolean
      halt_state: Boolean
      hog_wild: Boolean
      i_am_your_shield: Boolean
      mine_sweeper: Boolean
      overclocked: Boolean
      power_overwhelming: Boolean
      shot_down: Boolean
      storm_earth_and_fire: Boolean
      strike: Boolean
      the_power_of_attraction: Boolean
    }
  }

  heroes: {
    playtime: {
      competitive: HeroesPlaytime
      quickplay: HeroesPlaytime
    }
    stats: {
      competitive: HeroesStats
      quickplay: HeroesStats
    }
  }

  stats: {
    competitive: StatsComp
    quickplay: StatsQuick
  }
}
interface Hours extends Number { }
interface HeroesPlaytime {
  ana?: Hours
  bastion?: Hours
  brigitte?: Hours
  dva?: Hours
  genji?: Hours
  hanzo?: Hours
  junkrat?: Hours
  lucio?: Hours
  mccree?: Hours
  mei?: Hours
  mercy?: Hours
  moira?: Hours
  orisa?: Hours
  pharah?: Hours
  reaper?: Hours
  reinhardt?: Hours
  roadhog?: Hours
  soldier76?: Hours
  sombra?: Hours
  symmetra?: Hours
  tracer?: Hours
  widowmaker?: Hours
  wrecking_ball?: Hours
  zarya?: Hours
  zenyatta?: Hours
}
interface HeroesStats {
  ana?: HeroesHeroStats
  bastion?: HeroesHeroStats
  brigitte?: HeroesHeroStats
  dva?: HeroesHeroStats
  genji?: HeroesHeroStats
  hanzo?: HeroesHeroStats
  junkrat?: HeroesHeroStats
  lucio?: HeroesHeroStats
  mccree?: HeroesHeroStats
  mei?: HeroesHeroStats
  mercy?: HeroesHeroStats
  moira?: HeroesHeroStats
  orisa?: HeroesHeroStats
  pharah?: HeroesHeroStats
  reaper?: HeroesHeroStats
  reinhardt?: HeroesHeroStats
  roadhog?: HeroesHeroStats
  soldier76?: HeroesHeroStats
  sombra?: HeroesHeroStats
  symmetra?: HeroesHeroStats
  tracer?: HeroesHeroStats
  widowmaker?: HeroesHeroStats
  wrecking_ball?: HeroesHeroStats
  zarya?: HeroesHeroStats
  zenyatta?: HeroesHeroStats
}
interface HeroesHeroStats {
  general_stats: {
    [x: String]: Number
    all_damage_done: Number
    all_damage_done_most_in_game: Number
    all_damage_done_most_in_life: Number
    barrier_damage_done: Number
    barrier_damage_done_most_in_game: Number
    blaster_kills: Number
    blaster_kills_most_in_game: Number
    cards: Number
    critical_hit_accuracy: Number
    critical_hits: Number
    critical_hits_most_in_game: Number
    critical_hits_most_in_life: Number
    damage_amplified: Number
    damage_amplified_most_in_game: Number
    deaths: Number
    defensive_assists: Number
    defensive_assists_most_in_game: Number
    eliminations: Number
    eliminations_most_in_game: Number
    eliminations_most_in_life: Number
    eliminations_per_life: Number
    final_blows: Number
    final_blows_most_in_game: Number
    games_lost: Number
    games_played: Number
    games_won: Number
    healing_done: Number
    healing_done_most_in_game: Number
    hero_damage_done: Number
    hero_damage_done_most_in_game: Number
    hero_damage_done_most_in_life: Number
    kill_streak_best: Number
    medals: Number
    medals_bronze: Number
    medals_gold: Number
    medals_silver: Number
    melee_final_blow: Number
    melee_final_blow_most_in_game: Number
    objective_kills: Number
    objective_kills_most_in_game: Number
    objective_time: Number
    objective_time_most_in_game: Number
    offensive_assists: Number
    offensive_assists_most_in_game: Number
    players_resurrected: Number
    players_resurrected_most_in_game: Number
    secondary_fire_accuracy: Number
    self_healing: Number
    self_healing_most_in_game: Number
    time_played: Number
    time_spent_on_fire: Number
    time_spent_on_fire_most_in_game: Number
    weapon_accuracy: Number
    weapon_accuracy_best_in_game: Number
    win_percentage: Number
  }
  rolling_average_stats: {
    [x: String]: Number
    all_damage_done: Number
    barrier_damage_done: Number
    blaster_kills: Number
    critical_hits: Number
    damage_amplified: Number
    deaths: Number
    defensive_assists: Number
    eliminations: Number
    final_blows: Number
    healing_done: Number
    hero_damage_done: Number
    melee_final_blows: Number
    objective_kills: Number
    objective_time: Number
    offensive_assists: Number
    players_resurrected: Number
    self_healing: Number
    time_spent_on_fire: Number
  }
}
interface Stats {
  competitive: Boolean
  game_stats: {
    all_damage_done: Number
    all_damage_done_most_in_game: Number
    barrier_damage_done: Number
    barrier_damage_done_most_in_game: Number
    cards: Number
    damage_done: Number
    deaths: Number
    defensive_assists: Number
    defensive_assists_most_in_game: Number
    eliminations: Number
    eliminations_most_in_game: Number
    final_blows: Number
    final_blows_most_in_game: Number
    games_lost: Number
    games_played: Number
    games_won: Number
    healing_done: Number
    healing_done_most_in_game: Number
    hero_damage_done: Number
    hero_damage_done_most_in_game: Number
    kill_streak_best: Number
    kpd: Number
    medals: Number
    medals_bronze: Number
    medals_gold: Number
    medals_silver: Number
    melee_final_blow: Number
    melee_final_blow_most_in_game: Number
    objective_kills: Number
    objective_kills_most_in_game: Number
    objective_time: Number
    objective_time_most_in_game: Number
    offensive_assists: Number
    offensive_assists_most_in_game: Number
    solo_kills_most_in_game: Number
    time_played: Number
    time_spent_on_fire: Number
    time_spent_on_fire_most_in_game: Number
  }
  overall_stats: {
    avatar: URL
    comprank: Number?;
    endorsement_level: Number
    endorsement_shotcaller: Number
    endorsement_sportsmanship: Number
    endorsement_teammate: Number
    games: Number
    level: Number
    losses: Number
    prestige: Number?;
    tier: Number?;
    ties?: Number
    win_rate: Number
    wins: Number
  }
}
interface StatsComp extends Stats {
  competitive: true
}
interface StatsQuick extends Stats {
  competitive: false
}
