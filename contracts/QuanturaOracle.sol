// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title Quantura Oracle Contract
/// @notice Accepts AI decisions and post-quantum signature hashes

contract QuanturaOracle {
    address public admin;

    struct Result {
        address submitter;
        bytes32 dataHash;
        uint256 timestamp;
    }

    mapping(uint256 => Result) public results;
    uint256 public latestId;

    constructor() {
        admin = msg.sender;
    }

    /// @notice Submit hashed result from off-chain AI/PQ signature
    /// @param dataHash keccak256 hash of the AI or PQ output
    function submitResult(bytes32 dataHash) external {
        latestId += 1;
        results[latestId] = Result({
            submitter: msg.sender,
            dataHash: dataHash,
            timestamp: block.timestamp
        });
    }

    function getResult(uint256 id) external view returns (Result memory) {
        return results[id];
    }
}
