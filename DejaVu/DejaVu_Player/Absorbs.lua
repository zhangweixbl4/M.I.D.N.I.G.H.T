local addonName, addonTable = ... -- 插件入口固定写法

-- Lua 原生函数
local ipairs = ipairs
local After = C_Timer.After
local random = math.random
local min = math.min
local insert = table.insert

-- WoW 官方 API
local UnitGetTotalAbsorbs = UnitGetTotalAbsorbs
local UnitGetTotalHealAbsorbs = UnitGetTotalHealAbsorbs
local UnitHealthMax = UnitHealthMax

local DejaVu = _G["DejaVu"]
local Bar = DejaVu.Bar


After(2, function()
    local eventFrame = CreateFrame("Frame") -- 事件框架
    local damageAbsorbsBar = Bar:New(43, 16, 20)
    local healAbsorbsBar = Bar:New(64, 14, 20)

    -- 这两条都按玩家最大生命值做刻度, 直接把官方数值透传给 StatusBar。
    local function updateMaxHealth()
        local maxHealth = UnitHealthMax("player") or 0
        damageAbsorbsBar:setMinMaxValues(0, maxHealth)
        healAbsorbsBar:setMinMaxValues(0, maxHealth)
    end

    local function updateDamageAbsorbs()
        damageAbsorbsBar:setValue(UnitGetTotalAbsorbs("player") or 0)
    end

    local function updateHealAbsorbs()
        healAbsorbsBar:setValue(UnitGetTotalHealAbsorbs("player") or 0)
    end

    -- insert(UNIT_MAX_HEALTH_CHANGED, { unit = "player", func = updateMaxHealth })
    -- insert(UNIT_ABSORB_AMOUNT_CHANGED, { unit = "player", func = updateDamageAbsorbs })
    -- insert(UNIT_HEAL_ABSORB_AMOUNT_CHANGED, { unit = "player", func = updateHealAbsorbs })


    function eventFrame:UNIT_MAXHEALTH(unitToken)
        updateMaxHealth()
        updateDamageAbsorbs()
        updateHealAbsorbs()
    end

    function eventFrame:UNIT_ABSORB_AMOUNT_CHANGED(unitToken)
        updateDamageAbsorbs()
    end

    function eventFrame:UNIT_HEAL_ABSORB_AMOUNT_CHANGED(unitToken)
        updateHealAbsorbs()
    end

    eventFrame:RegisterUnitEvent("UNIT_MAXHEALTH", "player")
    eventFrame:RegisterUnitEvent("UNIT_ABSORB_AMOUNT_CHANGED", "player")
    eventFrame:RegisterUnitEvent("UNIT_HEAL_ABSORB_AMOUNT_CHANGED", "player")


    -- local fastTimeElapsed = -random()     -- 随机初始时间，避免所有事件在同一帧更新
    -- local lowTimeElapsed = -random()      -- 随机初始时间，避免所有事件在同一帧更新
    local superLowTimeElapsed = -random() -- 随机初始时间，避免所有事件在同一帧更新
    eventFrame:HookScript("OnUpdate", function(frame, elapsed)
        -- 每帧重置触发器状态，确保状态更新函数在同一帧内只执行一次

        -- fastTimeElapsed = fastTimeElapsed + elapsed
        -- if fastTimeElapsed > 0.1 then
        --     fastTimeElapsed = fastTimeElapsed - 0.1
        -- end
        -- lowTimeElapsed = lowTimeElapsed + elapsed
        -- if lowTimeElapsed > 0.5 then
        --     lowTimeElapsed = lowTimeElapsed - 0.5
        -- end
        superLowTimeElapsed = superLowTimeElapsed + elapsed
        if superLowTimeElapsed > 2 then
            superLowTimeElapsed = superLowTimeElapsed - 2
            updateMaxHealth()
            updateDamageAbsorbs()
            updateHealAbsorbs()
        end
    end)


    eventFrame:SetScript("OnEvent", function(self, event, ...)
        self[event](self, ...)
    end)
end)
