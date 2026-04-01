from __future__ import annotations

from terminal.context import Context
from .base import BaseRotation


class DruidGuardian(BaseRotation):
    name = "熊德"
    desc = "熊德旋转"

    def __init__(self) -> None:
        super().__init__()

        self.macroTable = {
            "target月火术": "ALT-NUMPAD1",
            "focus月火术": "ALT-NUMPAD2",
            "target裂伤": "ALT-NUMPAD3",
            "focus裂伤": "ALT-NUMPAD4",
            "target毁灭": "ALT-NUMPAD5",
            "focus毁灭": "ALT-NUMPAD6",
            "target摧折": "ALT-NUMPAD7",
            "focus摧折": "ALT-NUMPAD8",
            "target重殴": "ALT-NUMPAD9",
            "focus重殴": "ALT-NUMPAD0",
            "target赤红之月": "SHIFT-NUMPAD1",
            "focus赤红之月": "SHIFT-NUMPAD2",
            "target明月普照": "SHIFT-NUMPAD3",
            "focus明月普照": "SHIFT-NUMPAD4",
            "开怪痛击": "SHIFT-NUMPAD5",
            "补痛击": "SHIFT-NUMPAD5",
            "AOE痛击": "SHIFT-NUMPAD5",
            "填充横扫": "SHIFT-NUMPAD6",
            "any切换目标": "SHIFT-NUMPAD7",
            "player狂暴": "SHIFT-NUMPAD8",
            "player化身": "SHIFT-NUMPAD9",
            "低保铁鬃": "SHIFT-NUMPAD0",
            "泻怒铁鬃": "SHIFT-NUMPAD0",
            "狂暴回复": "ALT-F2",
            "树皮术": "ALT-F3",
            "player生存本能": "ALT-F5",
            "target迎头痛击": "ALT-F6",
            "focus迎头痛击": "ALT-F7",
            "any熊形态": "ALT-F8",
            "裂伤": "ALT-F9",
            "溢出裂伤": "ALT-F9",
            "补怒裂伤": "ALT-F9",
            "毁灭": "ALT-F10",
        }

    def main_rotation(self, ctx: Context) -> tuple[str, float, str]:
        GCD_QUEUE_WINDOW = 0.2
        AOE_ENEMY_COUNT = 4
        OPENER_TIME = 10.0
        FRENZIED_REGEN_THRESHOLD = 45.0
        BARKSKIN_THRESHOLD = 20.0
        SURVIVAL_INSTINCTS_THRESHOLD = 10.0
        RAGE_OVERFLOW_THRESHOLD = 100.0
        RAGE_MAUL_THRESHOLD = 100.0
        RAGE_MAX = 120.0
        USE_INCARNATION = True
        USE_IRONFUR = True
        INTERRUPT_WITH_FOCUS = True
        # print("==========================")
        if not ctx.enable:
            return self.idle("总开关未开启")

        if ctx.delay:
            return self.idle("延迟开关开启")

        player = ctx.player
        target = ctx.target
        focus = ctx.focus

        if not player.alive:
            return self.idle("玩家已死亡")

        if player.isChatInputActive:
            return self.idle("正在聊天输入")

        if player.isMounted:
            return self.idle("骑乘中")

        if player.castIcon is not None:
            return self.idle("正在施法")

        if player.channelIcon is not None:
            return self.idle("正在引导")

        if player.isEmpowering:
            return self.idle("正在蓄力")

        if player.hasBuff("食物和饮料"):
            return self.idle("正在吃喝")

        if not player.isInCombat:
            return self.idle("未进入战斗")

        if player.hasBuff("旅行形态"):
            return self.idle("旅行形态中")

        if not player.hasBuff("熊形态"):
            return self.cast("any熊形态")

        main_target = None
        if target.exists:
            if target.canAttack:
                if target.isInMeleeRange or target.isInRangedRange:
                    main_target = target
        if main_target is None:
            if focus.exists:
                if focus.canAttack:
                    if focus.isInMeleeRange or focus.isInRangedRange:
                        main_target = focus

        if main_target is None:
            return self.idle("需要一个敌对目标")

        spell_queue_window = float(ctx.spell_queue_window or GCD_QUEUE_WINDOW)
        gcd_ready = ctx.gcd_ready(spell_queue_window)

        player_health = float(player.healthPercent)
        rage = float(player.powerPercent) * RAGE_MAX / 100.0
        is_opener = float(ctx.combat_time) <= OPENER_TIME
        is_aoe = int(player.enemyCount) >= AOE_ENEMY_COUNT
        enemy_in_range = int(player.enemyCount) >= 1
        player_is_stand = not player.isMoving

        red_moon_spell = ctx.spell("赤红之月")
        if ctx.spell_cooldown_ready("赤红之月", spell_queue_window):
            if is_opener:
                return self.cast(f"{main_target.unitToken}赤红之月")

        if not main_target.hasDebuff("月火术"):
            if red_moon_spell is None or not red_moon_spell.is_known:
                if gcd_ready:
                    if is_opener:
                        return self.cast(f"{main_target.unitToken}月火术")
        # print("133")
        if player_health < FRENZIED_REGEN_THRESHOLD:
            if ctx.spell_charges_ready("狂暴回复", 1, spell_queue_window):
                return self.cast("狂暴回复")

        if player_health < BARKSKIN_THRESHOLD:
            if ctx.spell_cooldown_ready("树皮术", spell_queue_window):
                return self.cast("树皮术")

        if player_health < SURVIVAL_INSTINCTS_THRESHOLD:
            if ctx.spell_cooldown_ready("生存本能", spell_queue_window):
                return self.cast("player生存本能")
        # print("145")
        if USE_IRONFUR:
            if (not player.hasBuff("铁鬃")) or player.buffStack("铁鬃") < 2 or player.buffRemain("铁鬃") < 3:
                if ctx.spell_cooldown_ready("铁鬃", spell_queue_window, ignore_gcd=True):
                    return self.cast("低保铁鬃")

        if ctx.spell_cooldown_ready("痛击", spell_queue_window):
            if is_opener:
                if enemy_in_range:
                    return self.cast("开怪痛击")

        incarnation_ready = ctx.spell_cooldown_ready("化身", spell_queue_window, ignore_gcd=True)
        # print("157")
        if USE_INCARNATION:
            if incarnation_ready:
                if is_opener:
                    if player_is_stand:
                        return self.cast("player化身")

        if ctx.spell_cooldown_ready("狂暴", spell_queue_window):
            if is_opener:
                if player_is_stand:
                    return self.cast("player狂暴")

        if ctx.spell_cooldown_ready("迎头痛击", spell_queue_window, ignore_gcd=True):
            if INTERRUPT_WITH_FOCUS:
                if focus.exists:
                    if focus.canAttack:
                        if focus.isInMeleeRange or focus.isInRangedRange:
                            if focus.castIcon is not None and focus.castIsInterruptible:
                                return self.cast("focus迎头痛击")
                            if focus.channelIcon is not None and focus.channelIsInterruptible:
                                return self.cast("focus迎头痛击")
            if target.exists:
                if target.canAttack:
                    if target.isInMeleeRange or target.isInRangedRange:
                        if target.castIcon is not None and target.castIsInterruptible:
                            return self.cast("target迎头痛击")
                        if target.channelIcon is not None and target.channelIsInterruptible:
                            return self.cast("target迎头痛击")
        # print("185")
        if ctx.spell_cooldown_ready("明月普照", spell_queue_window):
            if is_opener:
                if player_is_stand:
                    return self.cast(f"{main_target.unitToken}明月普照")

        if ctx.spell_cooldown_ready("毁灭", spell_queue_window):
            if rage > 40:
                return self.cast("毁灭")
        # print("194")
        if ctx.spell_charges_ready("裂伤", 2, spell_queue_window):
            # spell = ctx.spell("裂伤")
            # if spell is not None:
            #     print(f"裂伤 charges: {spell.charges}, cooldown: {spell.cooldown}")
            if rage < RAGE_OVERFLOW_THRESHOLD:
                return self.cast("溢出裂伤")
        # print("198")
        if ctx.spell_cooldown_ready("痛击", spell_queue_window):
            if enemy_in_range:
                if main_target.debuffStack("痛击") < 3 or main_target.debuffRemain("痛击") < 4:
                    return self.cast("补痛击")
                if is_aoe:
                    return self.cast("AOE痛击")
        # print("205")
        if ctx.spell_charges_ready("裂伤", 1, spell_queue_window):
            if is_aoe:
                if rage <= RAGE_OVERFLOW_THRESHOLD:
                    return self.cast("补怒裂伤")
            else:
                return self.cast("裂伤")
        # print("213")
        if player.hasBuff("星河守护者"):
            if gcd_ready:
                if not is_aoe:
                    return self.cast(f"{main_target.unitToken}月火术")
                if player.buffRemain("星河守护者") < 4:
                    return self.cast(f"{main_target.unitToken}月火术")

        if not main_target.hasDebuff("月火术"):
            if gcd_ready:
                return self.cast(f"{main_target.unitToken}月火术")

        if rage > RAGE_MAUL_THRESHOLD:
            if is_aoe:
                if ctx.spell_cooldown_ready("摧折", spell_queue_window):
                    return self.cast("enemy摧折")
            else:
                if ctx.spell_cooldown_ready("重殴", spell_queue_window):
                    return self.cast(f"{main_target.unitToken}重殴")

        if rage > RAGE_OVERFLOW_THRESHOLD:
            if ctx.spell_cooldown_ready("铁鬃", spell_queue_window, ignore_gcd=True):
                return self.cast("泻怒铁鬃")

        if gcd_ready:
            if player.hasBuff("星河守护者"):
                return self.cast(f"{main_target.unitToken}月火术")
            return self.cast("填充横扫")

        return self.idle("当前没有合适动作")
