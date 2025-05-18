// SPDX-License-Identifier: MIT
pragma solidity ^0.8.24;

/// @title QuanturaDAO
/// @notice Basic token-based governance module for proposals and voting

interface IERC20 {
    function balanceOf(address account) external view returns (uint256);
}

contract QuanturaDAO {
    struct Proposal {
        string description;
        uint256 voteYes;
        uint256 voteNo;
        uint256 deadline;
        bool executed;
    }

    address public token;
    uint256 public proposalCount;
    mapping(uint256 => Proposal) public proposals;
    mapping(uint256 => mapping(address => bool)) public hasVoted;

    constructor(address _token) {
        token = _token;
    }

    function createProposal(string memory description) external {
        proposalCount++;
        proposals[proposalCount] = Proposal({
            description: description,
            voteYes: 0,
            voteNo: 0,
            deadline: block.timestamp + 3 days,
            executed: false
        });
    }

    function vote(uint256 proposalId, bool support) external {
        Proposal storage p = proposals[proposalId];
        require(block.timestamp < p.deadline, "Voting ended");
        require(!hasVoted[proposalId][msg.sender], "Already voted");

        uint256 weight = IERC20(token).balanceOf(msg.sender);
        require(weight > 0, "No voting power");

        if (support) {
            p.voteYes += weight;
        } else {
            p.voteNo += weight;
        }

        hasVoted[proposalId][msg.sender] = true;
    }

    function result(uint256 proposalId) external view returns (string memory) {
        Proposal memory p = proposals[proposalId];
        if (block.timestamp < p.deadline) return "Voting in progress";
        if (p.voteYes > p.voteNo) return "✅ Passed";
        if (p.voteYes < p.voteNo) return "❌ Rejected";
        return "⚖️ Tie";
    }
}
