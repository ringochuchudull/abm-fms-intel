Agent based modelling for financial stock market.
===================================================
(i) There are N agents and N/2 shares in the artificial stock market, each agent can
only own one share at most. At every time step, there are N/2 agents
who own shares and are potential sellers, while the N/2 agents who do not own
shares are potential buyers., If the agent i is a potential sellers, he will have a sell
price Ps(i), also if the he is a potential buyers, he will have a bid price Pb(i)

(ii) Initially we randomly set the buyers bid price Pb and sellers sell price Ps in a
symmetric range of prices distributed uniformly. Also stock price limitation is set
as: maximum price is maxP, and minimum price is 1.

(iii) In each step one agent is randomly chosen, it may be a potential buyer or seller.
Price updating rules are as follows.
    
    (a) His price Ps(i) or Pb(i) is updated according to rules: approaching ∆P to
    instant stock price, which is also the price in last step P(t−1), with probability
    (1 + D)/2, stepping away ∆P from instant stock price with probability
    (1 − D)/2. ∆P differs in different models. Here the drift parameter D is
    used to give agents a direction to update their price.

    (b) After updating his price, this agent will look into the entire market. If this
    agent owns a share, and observes that the price that one or more buyers who
    are willing to give is more than his sell price Pb(i), he will sell his share to the
    buyer who offers the highest price Ps(j). While if he wants to buy a share, and
    one or more buyers are willing to sell shares at less than his bid price Ps(i),
    he buys from the seller offering the lowest price Pb(j). If there is no price
    for which this agent wants to sell or buy, the procedure will go to the next
    step, and the stock price P(t) stays the same as P(t − 1). When a transaction
    happens, that price is the new stock P(t), which is bid or sell price of agent j.
    (c) After the transaction, seller in this transaction becomes a potential buyer, he
    will have a bid price Pb. And buyer becomes a potential seller, he will have a
    sell price Ps. New Pb and Ps are defined differently in different models.

================================
Useful resources:
    background material:
        http://pages.stern.nyu.edu/~jhasbrou/Teaching/POST%20Draft%20syllabus/powerpoints/dealers.pdf

    Structure of PalamAgent:
        Please refer to Section 3 of this link:
        https://webhome.phy.duke.edu/~palmer/papers/arob98.pdf

        Also 'Conditional-action agent': Artificial Economic Life: A Simple Model of a Stockmarket
        http://www2.econ.iastate.edu/tesfatsi/SFISTOCKDetailed.LT.htm

    Quantitative Research
        https://arxiv.org/pdf/1703.06840.pdf

Rough UML Diagram:

|------------------|               |------------------|
|     Agent        |               | 0IntelligentAgent|
|------------------|               |------------------|
|    +id           |               |   buy()          |
|    +shares       |               |   sell()         |
|    +sell_record  | --inherent--> |   resetprice()   |
|    +buy_record   |               |                  |
|    record()      |               |                  |
|    newact()      |               |                  | 
|------------------|               |----------------- |
        ^
        |
        |
        |
        v
|------------------|   
|     Market       |   
|------------------|     
|    populate()    |            
|  record_order()  |           
|   newtrade()     | 
|    run()         |  
|------------------| 
