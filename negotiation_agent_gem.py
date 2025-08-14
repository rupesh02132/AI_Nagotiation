# This is the agent that you will be playing against in the competition.
import json
import re
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass
from enum import Enum
from abc import ABC, abstractmethod
import random

# ============================================
# PART 1 & 2: DATA STRUCTURES & BASE AGENT (unchanged)
# ============================================

@dataclass
class Product:
    """Product being negotiated"""
    name: str
    category: str
    quantity: int
    quality_grade: str  # 'A', 'B', or 'Export'
    origin: str
    base_market_price: int  # Reference price for this product
    attributes: Dict[str, Any]

@dataclass
class NegotiationContext:
    """Current negotiation state"""
    product: Product
    your_budget: int  # Your maximum budget (NEVER exceed this)
    current_round: int
    seller_offers: List[int]  # History of seller's offers
    your_offers: List[int]  # History of your offers
    messages: List[Dict[str, str]]  # Full conversation history

class DealStatus(Enum):
    ONGOING = "ongoing"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    TIMEOUT = "timeout"

class BaseBuyerAgent(ABC):
    """Base class for all buyer agents"""
    
    def __init__(self, name: str):
        self.name = name
        self.personality = self.define_personality()
        
    @abstractmethod
    def define_personality(self) -> Dict[str, Any]:
        pass
    
    @abstractmethod
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        pass
    
    @abstractmethod
    def respond_to_seller_offer(self, context: NegotiationContext, seller_price: int, seller_message: str) -> Tuple[DealStatus, int, str]:
        pass
    
    @abstractmethod
    def get_personality_prompt(self) -> str:
        pass


# ============================================
# PART 3: HYPER-ADAPTIVE BUYER AGENT
# ============================================

class YourBuyerAgent(BaseBuyerAgent):
    """
    ANALYTICAL BUYER AGENT - HYPER-ADAPTIVE MODEL

    This agent uses a highly responsive strategy to ensure deals are made, even
    in the toughest scenarios, while maximizing profitability when possible.
    """
    
    def define_personality(self) -> Dict[str, Any]:
        return {
            "personality_type": "hyper-adaptive",
            "traits": ["strategic", "data-driven", "pragmatic", "firm"],
            "negotiation_style": "A highly responsive approach that analyzes seller movements and adapts quickly. It prioritizes deal completion in tight scenarios.",
            "catchphrases": ["Let's find a profitable solution.", "My data suggests a different value.", "This is the final offer I can make."]
        }
    
    def generate_opening_offer(self, context: NegotiationContext) -> Tuple[int, str]:
        """
        Generates a more aggressive opening offer to create a strong negotiation anchor.
        """
        market_price = context.product.base_market_price
        quality = context.product.quality_grade

        if quality in ["A", "Export"]:
            opening_percentage = 0.68  # Slightly more aggressive
        else:
            opening_percentage = 0.58
        
        opening_price = int(market_price * opening_percentage)
        opening_price = min(opening_price, context.your_budget)

        message = f"Hello. Based on my analysis, I believe a fair starting point for these {context.product.name} would be ₹{opening_price}. Let's find a profitable solution."
        
        return opening_price, message
    
    def respond_to_seller_offer(self, context: NegotiationContext, seller_price: int, seller_message: str) -> Tuple[DealStatus, int, str]:
        """
        Responds with a dynamic strategy that prioritizes deal completion in the final rounds.
        """
        market_price = context.product.base_market_price
        last_offer = context.your_offers[-1] if context.your_offers else 0
        
        # --- End-Game Strategy (Rounds 8-10) ---
        if context.current_round >= 8:
            # Check if the seller's price is within a small margin of our budget
            if seller_price <= context.your_budget:
                return DealStatus.ACCEPTED, seller_price, f"I've considered all factors, and I'll take your offer of ₹{seller_price}. Let's close the deal."

            # If not, make a final, non-negotiable offer just below the budget.
            # This is key to closing hard-scenario deals.
            final_offer = int(context.your_budget * 0.99) # 1% below budget
            final_offer = max(final_offer, last_offer + 1)
            
            # Ensure the final offer is a new, meaningful offer but still within a safe zone
            if final_offer > seller_price:
                 final_offer = int(seller_price * 0.99)

            return DealStatus.ONGOING, final_offer, f"This is the final offer I can make: ₹{final_offer}. I can't go any higher."

        # --- General Negotiation Strategy (Rounds 1-7) ---
        else:
            # Check for a good deal early on.
            if seller_price <= int(market_price * 0.85) and seller_price <= context.your_budget:
                return DealStatus.ACCEPTED, seller_price, f"That's a very fair price. I've run the numbers, and I can accept ₹{seller_price}."

            # Calculate a dynamic counter-offer based on seller's concession
            last_seller_offer = context.seller_offers[-2] if len(context.seller_offers) > 1 else seller_price
            seller_concession = last_seller_offer - seller_price
            
            # The buyer's counter-offer is a percentage of the seller's concession.
            # Be cautious early, more flexible as time passes.
            concession_rate = 0.2 + (context.current_round * 0.1) # increases over time
            increase_amount = int(seller_concession * concession_rate) if seller_concession > 0 else int(market_price * 0.02)
            
            counter_offer = last_offer + increase_amount
            
            # Final checks to ensure the offer is valid and a real counter
            counter_offer = min(counter_offer, seller_price - 1)
            counter_offer = min(counter_offer, context.your_budget)
            counter_offer = max(counter_offer, last_offer + 1)
            
            message = f"I appreciate your offer, but my data suggests a different value. I can move up to ₹{counter_offer}."
            
            return DealStatus.ONGOING, counter_offer, message

    def get_personality_prompt(self) -> str:
        return """
        I am a strategic and highly adaptive buyer who bases my decisions on objective data and negotiation flow. I maintain a calm and pragmatic tone, but my offers are calculated to be as efficient as possible. I use phrases like 'Let's find a profitable solution' and 'My data suggests a different value' to drive the conversation. In the final rounds, I will make a firm, non-negotiable offer to close the deal, even if it means accepting a lower profit margin to avoid a timeout.
        """