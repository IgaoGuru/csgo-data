#pragma once

#include <array>
#include <deque>

#include "../SDK/matrix3x4.h"
#include "../SDK/Vector.h"

enum class FrameStage;
struct UserCmd;

namespace Backtrack {
    void update(FrameStage) noexcept;
    void run(UserCmd*) noexcept;

    struct Record {
        Vector origin;
        float simulationTime;
        matrix3x4 matrix[256];
    };

    extern std::array<std::deque<Record>, 65> records;

    float getLerp() noexcept;
    bool valid(float simtime) noexcept;
    int timeToTicks(float time) noexcept;
    void init() noexcept;
}
