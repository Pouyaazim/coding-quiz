import math


def xp_for_level(level: int) -> int:
    """XP لازم برای رسیدن به این لول (از صفر)"""
    if level <= 0:
        return 0
    return 50 * (level ** 2)


def level_from_xp(xp: int) -> int:
    """از XP، لول رو حساب می‌کنه"""
    if xp <= 0:
        return 0
    return int(math.sqrt(xp / 50))


def level_progress(xp: int) -> dict:
    """
    اطلاعات کامل پیشرفت کاربر رو برمی‌گردونه:
    - level: لول فعلی
    - xp_current: XP فعلی
    - xp_level_start: XP شروع این لول
    - xp_next_level: XP لول بعدی
    - xp_in_level: XP جمع‌شده تو این لول
    - xp_needed: XP لازم برای این لول
    - progress: درصد پیشرفت (0-100)
    """
    level = level_from_xp(xp)

    xp_level_start = xp_for_level(level)
    xp_next_level = xp_for_level(level + 1)
    xp_needed = xp_next_level - xp_level_start
    xp_in_level = xp - xp_level_start

    progress = 0
    if xp_needed > 0:
        progress = round((xp_in_level / xp_needed) * 100, 1)

    return {
        "level": level,
        "xp_current": xp,
        "xp_level_start": xp_level_start,
        "xp_next_level": xp_next_level,
        "xp_in_level": xp_in_level,
        "xp_needed": xp_needed,
        "progress": progress,
    }