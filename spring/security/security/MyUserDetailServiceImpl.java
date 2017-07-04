package com.fwd.eprecious.service.security;

import java.util.Collection;
import java.util.HashSet;
import java.util.Set;

import org.springframework.security.core.GrantedAuthority;
import org.springframework.security.core.authority.SimpleGrantedAuthority;
import org.springframework.security.core.userdetails.UserDetails;
import org.springframework.security.core.userdetails.UserDetailsService;
import org.springframework.security.core.userdetails.UsernameNotFoundException;

import com.fwd.eprecious.dao.UserDao;
import com.fwd.eprecious.dto.UserDetail;


public class MyUserDetailServiceImpl implements UserDetailsService {
	
	private UserDao userDao;

	public void setUserDao(UserDao userDao) {
		this.userDao = userDao;
	}

	// login check
	public UserDetails loadUserByUsername(String username) throws UsernameNotFoundException {
		
		//get user
		com.fwd.eprecious.entity.User user = userDao.findUniqueByProperty("name",username);
		if  (user==null) {
			throw new UsernameNotFoundException(username+" not exist!");  
		}  
            
		Collection<GrantedAuthority> grantedAuths = obtionGrantedAuthorities(user);
		// wrap spring security user
		UserDetail userdetail = new UserDetail(
				user.getName(), 
				user.getPassword(),
				true, 
				true, 
				true,
				true, 
				grantedAuths	//用户的权限
			);
		userdetail.setId(user.getId());
		return userdetail;
	}

	//get user roles
	private Set<GrantedAuthority> obtionGrantedAuthorities(com.fwd.eprecious.entity.User user) {
		com.fwd.eprecious.entity.Role role = user.getRole();
		
		Set<GrantedAuthority> authSet = new HashSet<GrantedAuthority>();
		authSet.add(new SimpleGrantedAuthority("ROLE_" + role.getRoleName()));
		return authSet;
	}
}