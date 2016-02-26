using DataFrames

df = readtable("C:\\Users\\m1rab03\\Documents\\Projects\\Hedge_cleaned.csv")

choices = [string(c) for c in names(df)[2:end]]

hedges = DataFrame( broker=String[], p1=String[], p2=String[], p3=String[], p4=String[], ret=Float32[] )

for k in 1:size(df)[1]
    broker = df[k,:broker]
    function isvalidchoice(choice::String)
        return ~isna(df[k,symbol(choice)])
    end
    row_choices = filter(isvalidchoice, choices)
    currencies = Set([c[1:3] for c in row_choices])
    for c1 in currencies
        for c2 in currencies
            for c3 in currencies
                for c4 in currencies
                    if length(Set([c1, c2, c3, c4]))==4
                        comb = [c1*"_"*c2, c2*"_"*c3, c3*"_"*c4, c4*"_"*c1]
                        if all([in(col, row_choices) for col=comb]) 
                            p1, p2, p3, p4 = comb
                            ret = reduce(+, [df[k, symbol(col)] for col in comb])
                            push!(hedges, [broker p1 p2 p3 p4 ret])
                        end 
                    end
                end
            end
        end
    end
end
                    

sort!(hedges, cols=[:r], rev=true)
print(hedges)

broker_ret = sort!(by(hedges, [:broker], df -> median(df[:ret])), cols=[:x1], rev=true)
pos_ret = sort!(hedges[hedges[:ret] .> 1e-8, :], cols=[:ret], rev=true)
broker_ret = sort!(by(pos_ret, [:broker], df -> size(df)[1](df[:ret])), cols=[:x1], rev=true)
