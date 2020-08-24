# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    main.py                                            :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: myener <myener@student.42.fr>              +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2020/08/24 11:22:20 by myener            #+#    #+#              #
#    Updated: 2020/08/24 12:31:16 by myener           ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

all_products = {} # Dictionary containing all the products. Here we assume everything is in stock.
product_input = ""
product_found = # What AGATHA's cnn found, str
accuracy = # AGATHA's cnn's accuracy, float


def bluff():
	"""To be implemented. Advanced feature meant to trick the potential fraudster
	into admitting the fraud if and when the accuracy is so different it is almost
	certain fraud is occurring.
	"""
	pass

def main():
	"""This is the main program through which AGATHA's behavior is decided.
	The approach must be subtle enough so as not to interfere with a non-fraudster
	customer's buying experience.
	We therefore rely on a an accuracy threshold to decide how to approach the conflict.
	"""

	# First of all, a certain number of parameters must be present for AGATHA to
	# investigate. Otherwise, the risk/benefit ratio makes any intervention obsolete
	# (hence the "else: pass" as we might add features in the future).

	if product_input is not product_found and accuracy < 80.0:
		# Case in which fraud is most likely (where bluff() could be implemented):
		if accuracy < 50.0:
			answer = input("Are you sure ? Please confirm the product you are buying is {0}.".format(product_input))
			if answer.upper() is 'Y':
				#call_security()
				print("Please wait, store personnel will be with you shortly.")
				# After reading this, if they're wise, they'll just leave.
			elif answer.upper() is 'N':
				answer = input("Please enter the actual name of the product.")
				if answer in all_products:
					product_input = answer
					main()
				else:
					while answer not in all_products:
						answer = input("Product not found. Please enter a correct product name.")

		# Case in which fraud is less likely:
		else:
			answer = input("Please confirm the product you are buying is {0} and not {1}.".format(product_input, product_found))
			if answer.upper() is 'Y':
				pass
				# This part I am not sure of. Do we let them go ? Do we call store personnel w/o security? (To be confirmed though a fraud-repression consulting)
			elif answer.upper() is 'N':
				answer = input("Please confirm you are buying {1}.".format(product_input, product_found))
				if answer.upper() is 'Y':
					product_input = product_found
					main()
				elif answer.upper() is 'N':
					answer = input("Please enter the actual name of the product.")
						if answer in all_products:
							product_input = answer
							main()
						else:
							while answer not in all_products:
								answer = input("Product not found. Please enter a correct product name.")
	# Case in which an error is more likely than a fraud:
	else:
		pass