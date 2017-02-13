#pragma once

#include "pire/encoding.h"


namespace Pire {
namespace PythonBinding {

yvector<wchar32> Utf8ToUcs4(const char* begin, const char* end) {
    yvector<wchar32> ucs4;
    Encodings::Utf8().FromLocal(begin, end, std::back_inserter(ucs4));
    return ucs4;
}
}  // PythonBinding
}  // Pire
