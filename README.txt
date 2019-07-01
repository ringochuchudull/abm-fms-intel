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



Notes:
http://www2.econ.iastate.edu/classes/econ308/tesfatsion/SFIStockOverview.LT.pdf
https://pdf.sciencedirectassets.com/278653/1-s2.0-S1877705811X0019X/1-s2.0-S1877705811054336/main.pdf?x-amz-security-token=AgoJb3JpZ2luX2VjEFkaCXVzLWVhc3QtMSJIMEYCIQDyATXxpk000JAHoMNE3QVBzvQ6F5ZQ%2BQCbAuIsoeM1EQIhAINVyK34mBfRk2UfZ58H4Ljf1puqCz%2FfFMXEaK4%2Fp1B3KuMDCKL%2F%2F%2F%2F%2F%2F%2F%2F%2F%2FwEQAhoMMDU5MDAzNTQ2ODY1Igzgk8qLyo7jEcBXcmIqtwMx4uKYJGu8lISfh6YAGnDtBcz5NvX9qSa3gDi%2FLIPZWFVQdllXCHKjKfYgGEoUPQdVeBOyXV%2BeLe8HLTCg5m%2FZTF4SGOBOztyEMt06%2BqNIt8C78%2F0OoNqT5%2BjF%2FQwkkYSodkZdCV%2BOlUh1dy1ZFLiEKuWFyMFyLjcbwEHrwFnAUwW96T9lfN8%2FaFUhVRA%2B5dahs0kz7x0NU%2BaUmE%2BOmyMLeQhw%2Bj9o%2BgaZDrnsSqVSln6pesAYIV9lFpM880cuNQva1WLJFMyZq%2FaZEp%2BDnjpFk7or7ED6dph1HHVDSOSbRUVSM3nqi1MZdBxO4P17l9jsGS%2B54Z3HfptJgQMOeHBV8KeA5N4yqj%2BkgJN0FvaTx81bvmBOu7rUIhFGK4cFnF7p7GWV8%2F8X9AeidfFR23FbMVyyWSUZI1OB3LDzVMQ2d6VbqCDY8wqGYv6UPeKrfejpA%2BFomkWG76dqy9zqumS8Vcq1H4d3uRV3rfHW6JgtCcggtx577S07kmbUZL7ptDfuyvWYM78qgyYg4SzzdXajp7rB6Vq6hv3K8BwyBCw2NTWBjKxBES9HrXCnJyOK2n8pHOkE1OsHMPuI5%2BgFOrMBFd4QaXO1S2r27mPtcaiQwAXNjtYidnaCsIOcFW2JDdcGAZaLhmA6lueFZjH2PTpwGCKT05PtFDql%2FKoebj%2F00hLvDgCUcGkXVqMqhzczgXvLno9QecWyRrZb%2BM7Srlp8mfxMc%2FLYSkRhA8ONlSmf4JyrKKb79477z5PMJ%2FWwzWsIJkZgnWfR%2FlmOvPPEVFZYzPsXQaA8igzpIJ9vlroWNMgLkT5OsgUzay9znZVWjxSlJMw%3D&AWSAccessKeyId=ASIAQ3PHCVTY3H65SEEI&Expires=1561973723&Signature=UwnKGSyIbasE9b2QkQRNUs%2FK2ZU%3D&hash=5e7df56246be2610d3004bd565ca84c1188adbddec1b23428264f89bf1f5dbec&host=68042c943591013ac2b2430a89b270f6af2c76d8dfd086a07176afe7c76c2c61&pii=S1877705811054336&tid=spdf-eb097272-29bb-4d8c-9712-099f4c92d89a&sid=b750145e6e968744da189f925bbed3d1aadcgxrqb&type=client