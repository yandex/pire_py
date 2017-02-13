#pragma once

#include "pire/pire.h"
#include "pire/easy.h"
#include "pire/extra.h"

#include <unordered_set>


namespace Pire {
namespace PythonBinding {

enum OptionFlag {
    % for option in OPTIONS:
    ${option},
    % endfor
};

typedef std::unordered_set<OptionFlag> FlagSet;

inline yauto_ptr<Options> ConvertFlagSetToOptions(const FlagSet& options) {
    yauto_ptr<Options> converted(new Options());
    % for option, spec in OPTIONS.items():
    if (options.count(${option})) {
        converted->Add(${spec.cpp_getter});
    }
    % endfor
    return converted;
}
}  // PythonBinding
}  // Pire
// vim: ft=cpp
