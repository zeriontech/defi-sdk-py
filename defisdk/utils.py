from binascii import unhexlify
from decimal import Decimal
from typing import Any, Callable, List, Union

from sha3 import keccak_256

from .enums import AdapterType


def remove_0x_prefix(passed_hash: str) -> str:
    return passed_hash[2:] if passed_hash.startswith("0x") else passed_hash


def represent_address(address: str) -> str:
    address = address.lower()
    return address if address.startswith('0x') else f'0x{address}'


def represent_hash(passed_hash: Union[bytes, str]) -> str:
    passed_hash = passed_hash.hex() if isinstance(passed_hash, bytes) else passed_hash
    return passed_hash if passed_hash.startswith('0x') else f'0x{passed_hash}'


def hash_to_signature(passed_hash: str) -> str:
    passed_hash = remove_0x_prefix(passed_hash)
    return represent_hash(passed_hash[:8])


def hash_to_int(passed_hash: str, unsigned: bool = True) -> int:
    passed_hash = remove_0x_prefix(passed_hash)[:64]
    passed_hash = passed_hash.zfill(64)
    if not unsigned and int(passed_hash[0], 16) >= 8: # negative int
        return int(passed_hash, 16) - 2**256
    return int(passed_hash, 16)


def hash_to_decimal(passed_hash: str, decimals: int = 18) -> Decimal:
    value = hash_to_int(passed_hash)
    sign = int(value <= 0)
    digits = tuple(int(digit) for digit in str(abs(value)))
    exponent = -decimals
    return Decimal((sign, digits, exponent))


def hash_to_bool(passed_hash: str) -> bool:
    return hash_to_int(passed_hash) != 0


def hash_to_address(passed_hash: str) -> str:
    passed_hash = remove_0x_prefix(passed_hash)
    return f'0x{passed_hash[-40:]}'


def hash_to_words(passed_hash: str) -> List[str]:
    passed_hash = remove_0x_prefix(passed_hash)
    return [passed_hash[i:i + 64] for i in range(0, len(passed_hash), 64)]


def words_to_address(words: List[str]) -> str:
    return hash_to_address(words[0])


def words_to_int(words: List[str]) -> int:
    return hash_to_int(words[0])


def words_to_string(words: List[str]) -> str:
    string_length = hash_to_int(words[0]) * 2
    hex_string = ''.join(words[1:])
    return unhexlify(hex_string[:string_length]).decode()


def hash_to_list(
        passed_hash: str,
        serializer: Callable[[List[str]], Any] = words_to_address,
        dynamic_elements: bool = False
) -> List[Any]:
    return words_to_list(hash_to_words(passed_hash), serializer, dynamic_elements)


def words_to_list(
        words: List[str],
        serializer: Callable[[List[str]], Any],
        dynamic_elements: bool = False
) -> List[Any]:
    if not words:
        return []

    array_start = hash_to_int(words[0]) // 32
    array_length = hash_to_int(words[array_start])

    if array_length == 0:
        return []
    if dynamic_elements:
        element_positions = [
            hash_to_int(words[i]) // 32 for i in range(array_start + 1, array_start + 1 + array_length)
        ]
    else:
        element_positions = list(range(array_start - 1, array_start - 1 + array_length))

    result = []
    for i, position in enumerate(element_positions):
        start_position = array_start + 1 + position
        if i + 1 < len(element_positions):
            end_position = array_start + 1 + element_positions[i + 1]
            result.append(serializer(words[start_position:end_position]))
        else:
            result.append(serializer(words[start_position:]))
    return result


def get_signature_hash(signature: bytes) -> str:
    full_hash = keccak_256(signature).hexdigest()
    return hash_to_signature(full_hash)


def string_to_hash(passed_string: str) -> str:
    return represent_hash(bytes(passed_string, 'UTF-8'))


def get_adapter_id(adapter_name: str, adapter_type: AdapterType) -> str:
    encoded_adapter_name = string_to_hash(adapter_name)
    return string_to_hash(adapter_name) + '0' * (65 - len(encoded_adapter_name)) + str(adapter_type.value)
