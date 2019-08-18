/* HOW TO MAINTAIN THIS FILE:
 * Every time a new hero is realeased, update the Hero type by adding the new hero name like this: 'previous hero' | 'new hero' | 'following hero'
 */

type Hero = 'ana' | 'baptiste' | 'bastion' | 'brigitte' | 'dva' | 'genji' | 'hanzo' | 'junkrat' | 'lucio' | 'mccree' | 'mei' | 'mercy' | 'moira' | 'orisa' | 'pharah' | 'reaper' | 'reinhardt' | 'roadhog' | 'sigma' | 'soldier76' | 'sombra' | 'symmetra' | 'tracer' | 'widowmaker' | 'wrecking_ball' | 'zarya' | 'zenyatta'

export interface OWAPIBlob {
  _request: {
    api_ver: number
    route: string
  }

  any: null | Region;
  eu?: Region;
  kr?: Region;
  us?: Region;

  msg?: string;
  error?: number | 'Private';
}

export interface ErrorResponse extends OWAPIBlob {
  msg: string;
  error: number | 'Private';
  exc?: string
}

export interface Region {
  achievements: {
    damage: {
      [x: string]: boolean
      air_strike: boolean
      armor_up: boolean
      charge: boolean
      clearing_the_area: boolean
      cold_snap: boolean
      cratered: boolean
      death_from_above: boolean
      did_that_sting: boolean
      die_die_die_die: boolean
      hack_the_planet: boolean
      huge_success: boolean
      ice_blocked: boolean
      its_high_noon: boolean
      mine_like_a_steel_trap: boolean
      power_outage: boolean
      raid_wipe: boolean
      roadkill: boolean
      rocket_man: boolean
      served_up: boolean
      short_fuse: boolean
      simple_geometry: boolean
      slice_and_dice: boolean
      smooth_as_silk: boolean
      special_delivery: boolean
      target_rich_environment: boolean
      the_car_wash: boolean
      the_dragon_is_sated: boolean
      their_own_worst_enemy: boolean
      total_recall: boolean
      triple_threat: boolean
      waste_not_want_not: boolean
      whoa_there: boolean
    }
    general: {
      [x: string]: boolean
      blackjack: boolean
      centenary: boolean
      decked_out: boolean
      decorated: boolean
      level_10: boolean
      level_25: boolean
      level_50: boolean
      survival_expert: boolean
      the_friend_zone: boolean
      the_path_is_closed: boolean
      undying: boolean
    }
    maps: {
      [x: string]: boolean
      cant_touch_this: boolean
      double_cap: boolean
      escort_duty: boolean
      lockdown: boolean
      shutout: boolean
      world_traveler: boolean
    }
    special: {
      [x: string]: boolean
      a_couple_of_flakes: boolean
      a_quiet_night: boolean
      ambush: boolean
      clean_getaway: boolean
      cleanup_duty: boolean
      cool_as_ice: boolean
      dawn_breaks: boolean
      dawn_patrol: boolean
      distinguished_service: boolean
      flagbearer: boolean
      four_they_were: boolean
      handle_with_care: boolean
      hardened_defenders: boolean
      held_the_door: boolean
      hot_hand: boolean
      into_the_shadows: boolean
      lucio_hat_trick: boolean
      mission_complete: boolean
      not_a_scratch: boolean
      plausible_deniability: boolean
      rampage: boolean
      redacted: boolean
      replacements: boolean
      safe_hands: boolean
      six_they_were: boolean
      six_wanderers: boolean
      snowed_in: boolean
      strike_team: boolean
      survived_the_night: boolean
      survivor: boolean
      the_venice_incident: boolean
      thinking_with_your_stomach: boolean
      unit_commendation: boolean
      unscathed: boolean
      volley: boolean
      whap: boolean
      yeti_catcher: boolean
    }
    support: {
      [x: string]: boolean
      antipode: boolean
      enabler: boolean
      excuse_me: boolean
      grounded: boolean
      group_health_plan: boolean
      huge_rez: boolean
      naptime: boolean
      rapid_discord: boolean
      simple_trigonometry: boolean
      supersonic: boolean
      the_floor_is_lava: boolean
      the_iris_embraces_you: boolean
    }
    tank: {
      [x: string]: boolean
      adaptation: boolean
      anger_management: boolean
      game_over: boolean
      giving_you_the_hook: boolean
      halt_state: boolean
      hog_wild: boolean
      i_am_your_shield: boolean
      mine_sweeper: boolean
      overclocked: boolean
      power_overwhelming: boolean
      shot_down: boolean
      storm_earth_and_fire: boolean
      strike: boolean
      the_power_of_attraction: boolean
      event_horizon: boolean
      conservation_of_energy: boolean
    }
  }

  heroes: {
    playtime: {
      competitive: Record<Hero, Hours>
      quickplay: Record<Hero, Hours>
    }
    stats: {
      competitive: Record<Hero, HeroStats>
      quickplay: Record<Hero, HeroStats>
    }
  }

  stats: {
    competitive: StatsComp
    quickplay: StatsQuick
  }
}
interface Hours extends Number { }
interface HeroStats {
  general_stats: {
    [x: string]: number
    all_damage_done: number
    all_damage_done_most_in_game: number
    all_damage_done_most_in_life: number
    barrier_damage_done: number
    barrier_damage_done_most_in_game: number
    blaster_kills: number
    blaster_kills_most_in_game: number
    cards: number
    critical_hit_accuracy: number
    critical_hits: number
    critical_hits_most_in_game: number
    critical_hits_most_in_life: number
    damage_amplified: number
    damage_amplified_most_in_game: number
    deaths: number
    defensive_assists: number
    defensive_assists_most_in_game: number
    eliminations: number
    eliminations_most_in_game: number
    eliminations_most_in_life: number
    eliminations_per_life: number
    final_blows: number
    final_blows_most_in_game: number
    games_lost: number
    games_played: number
    games_won: number
    healing_done: number
    healing_done_most_in_game: number
    hero_damage_done: number
    hero_damage_done_most_in_game: number
    hero_damage_done_most_in_life: number
    kill_streak_best: number
    medals: number
    medals_bronze: number
    medals_gold: number
    medals_silver: number
    melee_final_blow: number
    melee_final_blow_most_in_game: number
    objective_kills: number
    objective_kills_most_in_game: number
    objective_time: number
    objective_time_most_in_game: number
    offensive_assists: number
    offensive_assists_most_in_game: number
    players_resurrected: number
    players_resurrected_most_in_game: number
    secondary_fire_accuracy: number
    self_healing: number
    self_healing_most_in_game: number
    time_played: number
    time_spent_on_fire: number
    time_spent_on_fire_most_in_game: number
    weapon_accuracy: number
    weapon_accuracy_best_in_game: number
    win_percentage: number
  }
  rolling_average_stats: {
    [x: string]: number
    all_damage_done: number
    barrier_damage_done: number
    blaster_kills: number
    critical_hits: number
    damage_amplified: number
    deaths: number
    defensive_assists: number
    eliminations: number
    final_blows: number
    healing_done: number
    hero_damage_done: number
    melee_final_blows: number
    objective_kills: number
    objective_time: number
    offensive_assists: number
    players_resurrected: number
    self_healing: number
    time_spent_on_fire: number
  }
}
interface Stats {
  competitive: boolean
  game_stats: {
    all_damage_done: number
    all_damage_done_most_in_game: number
    barrier_damage_done: number
    barrier_damage_done_most_in_game: number
    cards: number
    damage_done: number
    deaths: number
    defensive_assists: number
    defensive_assists_most_in_game: number
    eliminations: number
    eliminations_most_in_game: number
    final_blows: number
    final_blows_most_in_game: number
    games_lost: number
    games_played: number
    games_won: number
    healing_done: number
    healing_done_most_in_game: number
    hero_damage_done: number
    hero_damage_done_most_in_game: number
    kill_streak_best: number
    kpd: number
    medals: number
    medals_bronze: number
    medals_gold: number
    medals_silver: number
    melee_final_blow: number
    melee_final_blow_most_in_game: number
    objective_kills: number
    objective_kills_most_in_game: number
    objective_time: number
    objective_time_most_in_game: number
    offensive_assists: number
    offensive_assists_most_in_game: number
    solo_kills_most_in_game: number
    time_played: number
    time_spent_on_fire: number
    time_spent_on_fire_most_in_game: number
  }
  overall_stats: {
    avatar: string
    comprank?: number;
    endorsement_level: number
    endorsement_shotcaller: number
    endorsement_sportsmanship: number
    endorsement_teammate: number
    games: number
    level: number
    losses: number
    prestige?: number;
    tier?: number;
    ties?: number
    win_rate: number
    wins: number
  }
}
interface StatsComp extends Stats {
  competitive: true
}
interface StatsQuick extends Stats {
  competitive: false
}
